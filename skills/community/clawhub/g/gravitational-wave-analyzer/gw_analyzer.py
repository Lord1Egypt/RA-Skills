"""
Gravitational Wave Event Analyzer
==================================
Fetch real LIGO/Virgo/KAGRA strain data from GWOSC and run full signal analysis.

Usage:
    python gw_analyzer.py --event GW150914 --detector H1 --output ./output/
    python gw_analyzer.py --list-events --catalog GWTC-3 --top 10
    python gw_analyzer.py --event GW231123_135430 --detector L1 --output ./output/

Requirements:
    pip install gwpy gwosc numpy scipy matplotlib astropy
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

try:
    from gwpy.timeseries import TimeSeries
    from gwpy.frequencyseries import FrequencySeries
    from gwosc.catalog import EventTable
    from gwosc import datasets
    import gwosc.api as gwosc_api
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("Install with: pip install gwpy gwosc numpy scipy matplotlib astropy")
    sys.exit(1)


# ─── Constants ────────────────────────────────────────────────────────────────

CATALOGS = ["GWTC-1", "GWTC-2", "GWTC-2.1", "GWTC-3", "O4_Discovery_Papers"]
DETECTORS = ["H1", "L1", "V1", "K1"]
SAMPLE_RATE = 4096  # Hz
SEGMENT_DURATION = 32  # seconds around event
BANDPASS_LOW = 30    # Hz
BANDPASS_HIGH = 350  # Hz

# Merger classification thresholds (component masses in solar masses)
NS_MAX_MASS = 3.0  # anything below = neutron star


# ─── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class EventInfo:
    name: str
    catalog: str
    gps_time: float
    mass1: Optional[float]
    mass2: Optional[float]
    merger_type: str
    far: Optional[float]          # False alarm rate (Hz)
    network_snr: Optional[float]
    luminosity_distance_mpc: Optional[float]
    chirp_mass: Optional[float]


@dataclass
class AnalysisResult:
    event: EventInfo
    detector: str
    snr_estimate: float
    peak_freq_hz: float
    chirp_duration_s: float
    output_dir: str


# ─── Core Analyzer ────────────────────────────────────────────────────────────

class GWEventAnalyzer:
    """Full gravitational wave event analysis pipeline using GWOSC public data."""

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Catalog ───────────────────────────────────────────────────────────────

    def list_events(self, catalog: str = "GWTC-3", top: int = 10) -> list[dict]:
        """Fetch events from GWOSC catalog and return top N sorted by network SNR."""
        print(f"\n📡 Fetching events from catalog: {catalog}")
        try:
            table = EventTable.fetch(catalog)
            events = table.to_pandas()
        except Exception as e:
            print(f"[WARN] EventTable fetch failed: {e}")
            print("Falling back to GWOSC v2 API...")
            try:
                # Use direct API to list events
                url = f"https://gwosc.org/api/v2/events/?catalog={catalog}&format=json"
                import requests
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                raw = resp.json()
                event_list = raw.get("events", [])
                event_names = [ev.get("commonName", ev.get("name", "?")) for ev in event_list[:top]]
            except Exception as e2:
                print(f"[WARN] API fallback also failed: {e2}. Using known events.")
                event_names = ["GW150914", "GW170814", "GW170817", "GW190412",
                               "GW190521", "GW200105", "GW200115", "GW231123_135430"][:top]

            events_list = [{"name": n} for n in event_names]
            for ev in events_list:
                print(f"  • {ev['name']}")
            return events_list

        # Sort by SNR descending if available
        snr_col = next((c for c in events.columns if "snr" in c.lower()), None)
        if snr_col:
            events = events.sort_values(snr_col, ascending=False)

        top_events = events.head(top)
        print(f"\n{'Name':<30} {'Type':<8} {'SNR':<10} {'Dist (Mpc)':<12}")
        print("─" * 64)

        results = []
        for _, row in top_events.iterrows():
            name = row.get("name", row.get("commonName", "Unknown"))
            m1 = row.get("mass_1_source", None)
            m2 = row.get("mass_2_source", None)
            snr = row.get("network_matched_filter_snr", None)
            dist = row.get("luminosity_distance", None)
            mtype = _classify_merger(m1, m2)

            print(f"{name:<30} {mtype:<8} {str(round(snr,1) if snr else '?'):<10} {str(round(dist,0) if dist else '?'):<12}")
            results.append({
                "name": name, "type": mtype,
                "snr": snr, "distance_mpc": dist,
                "mass1": m1, "mass2": m2
            })

        return results

    # ── Full Event Analysis ───────────────────────────────────────────────────

    def analyze_event(
        self,
        event_name: str,
        detector: str = "H1",
        duration: int = SEGMENT_DURATION
    ) -> AnalysisResult:
        """
        Full analysis pipeline for a single GW event:
        1. Fetch event metadata
        2. Download strain data
        3. Process signal (whiten, filter)
        4. Compute Q-transform spectrogram
        5. Estimate SNR
        6. Generate plots + JSON report
        """
        print(f"\n🔭 Analyzing event: {event_name} | Detector: {detector}")

        # ── Step 1: Metadata ─────────────────────────────────────────────────
        event_info = self._fetch_event_metadata(event_name)
        print(f"   ✓ GPS time: {event_info.gps_time}")
        print(f"   ✓ Merger type: {event_info.merger_type}")
        if event_info.chirp_mass:
            print(f"   ✓ Chirp mass: {event_info.chirp_mass:.1f} M☉")
        if event_info.luminosity_distance_mpc:
            print(f"   ✓ Distance: {event_info.luminosity_distance_mpc:.0f} Mpc")

        # ── Step 2: Download Strain ──────────────────────────────────────────
        gps = event_info.gps_time
        strain = self._download_strain(event_name, detector, gps, duration)
        if strain is None:
            raise RuntimeError(f"Could not download strain data for {event_name} / {detector}")
        print(f"   ✓ Strain downloaded: {len(strain)} samples @ {strain.sample_rate.value:.0f} Hz")

        # ── Step 3: Signal Processing ────────────────────────────────────────
        strain_filtered = self._process_strain(strain)
        print(f"   ✓ Signal processed (whitened + bandpass filtered)")

        # ── Step 4: Q-Transform ──────────────────────────────────────────────
        print(f"   ✓ Computing Q-transform spectrogram...")
        q_gram = strain_filtered.q_transform(
            outseg=(gps - 0.5, gps + 0.5),
            qrange=(4, 64),
            frange=(BANDPASS_LOW, BANDPASS_HIGH),
        )

        # ── Step 5: SNR Estimate ─────────────────────────────────────────────
        snr_est = self._estimate_snr(strain_filtered, gps)
        peak_freq = self._estimate_peak_freq(strain_filtered)
        chirp_dur = self._estimate_chirp_duration(strain, gps)
        print(f"   ✓ Estimated SNR: {snr_est:.1f}")

        # ── Step 6: Plot & Report ────────────────────────────────────────────
        self._plot_full_analysis(
            event_name, detector, strain, strain_filtered, q_gram, gps
        )
        result = AnalysisResult(
            event=event_info,
            detector=detector,
            snr_estimate=snr_est,
            peak_freq_hz=peak_freq,
            chirp_duration_s=chirp_dur,
            output_dir=str(self.output_dir),
        )
        self._save_report(result)
        print(f"\n✅ Analysis complete! Output saved to: {self.output_dir}/")
        return result

    # ── Metadata ─────────────────────────────────────────────────────────────

    def _fetch_event_metadata(self, event_name: str) -> EventInfo:
        """Fetch event parameters from GWOSC API."""
        try:
            info = gwosc_api.fetch_event_json(event_name)
            events_dict = info.get("events", {})
            # Keys are versioned e.g. "GW150914-v4"; pick the latest
            matching_keys = sorted(
                [k for k in events_dict if k.startswith(event_name)],
                reverse=True
            )
            key = matching_keys[0] if matching_keys else event_name
            params = events_dict.get(key, {})

            gps = params.get("GPS", 0)
            catalog = params.get("catalog.shortName", "GWTC")

            # Grab best-estimate (median) params
            m1 = _get_param(params, "mass_1_source")
            m2 = _get_param(params, "mass_2_source")
            chirp = _get_param(params, "chirp_mass_source")
            dist = _get_param(params, "luminosity_distance")
            far = _get_param(params, "far")
            snr = _get_param(params, "network_matched_filter_snr")

        except Exception as e:
            print(f"   [WARN] GWOSC API error: {e}. Using fallback GPS.")
            gps = datasets.event_gps(event_name)
            catalog, m1, m2, chirp, dist, far, snr = "Unknown", None, None, None, None, None, None

        return EventInfo(
            name=event_name,
            catalog=catalog,
            gps_time=gps,
            mass1=m1,
            mass2=m2,
            merger_type=_classify_merger(m1, m2),
            far=far,
            network_snr=snr,
            luminosity_distance_mpc=dist,
            chirp_mass=chirp,
        )

    # ── Strain Download ───────────────────────────────────────────────────────

    def _download_strain(
        self,
        event_name: str,
        detector: str,
        gps: float,
        duration: int,
    ) -> Optional[TimeSeries]:
        """Download strain data centered on the event GPS time."""
        start = gps - duration / 2
        end = gps + duration / 2
        print(f"   ⬇  Downloading strain: {detector} [{start:.0f} – {end:.0f}]")
        try:
            strain = TimeSeries.fetch_open_data(detector, start, end, sample_rate=SAMPLE_RATE, cache=True)
            return strain
        except Exception as e:
            print(f"   [ERROR] Download failed: {e}")
            return None

    # ── Signal Processing ─────────────────────────────────────────────────────

    def _process_strain(self, strain: TimeSeries) -> TimeSeries:
        """Whiten and bandpass filter the strain."""
        # Whiten to flatten PSD
        white = strain.whiten(fftlength=4, overlap=2)
        # Bandpass to gravitational wave band
        filtered = white.bandpass(BANDPASS_LOW, BANDPASS_HIGH)
        return filtered

    # ── Analysis Helpers ──────────────────────────────────────────────────────

    def _estimate_snr(self, strain: TimeSeries, gps: float, window: float = 0.2) -> float:
        """Simple SNR estimate: peak amplitude / RMS of off-signal noise."""
        data = strain.value
        dt = strain.dt.value
        t0 = strain.t0.value
        times = t0 + np.arange(len(data)) * dt

        signal_mask = np.abs(times - gps) < window
        noise_mask = np.abs(times - gps) > 5.0

        if signal_mask.sum() == 0 or noise_mask.sum() == 0:
            return 0.0

        peak = np.max(np.abs(data[signal_mask]))
        noise_rms = np.sqrt(np.mean(data[noise_mask] ** 2))
        return float(peak / noise_rms) if noise_rms > 0 else 0.0

    def _estimate_peak_freq(self, strain: TimeSeries) -> float:
        """Estimate peak frequency via FFT of central 1s."""
        center = len(strain) // 2
        half = int(strain.sample_rate.value * 0.5)
        segment = strain.value[center - half: center + half]
        fft = np.abs(np.fft.rfft(segment))
        freqs = np.fft.rfftfreq(len(segment), d=strain.dt.value)
        mask = (freqs >= BANDPASS_LOW) & (freqs <= BANDPASS_HIGH)
        if not mask.any():
            return 0.0
        return float(freqs[mask][np.argmax(fft[mask])])

    def _estimate_chirp_duration(self, strain: TimeSeries, gps: float) -> float:
        """Rough chirp duration estimate."""
        t0 = strain.t0.value
        end = t0 + len(strain) * strain.dt.value
        # Just return segment around event
        return min(2.0, (gps - t0), (end - gps))

    # ── Plotting ──────────────────────────────────────────────────────────────

    def _plot_full_analysis(
        self, event_name, detector, strain_raw, strain_filtered, q_gram, gps
    ):
        """Generate a 3-panel analysis figure."""
        fig = plt.figure(figsize=(14, 10), facecolor="#0d0d0d")
        gs = GridSpec(3, 1, figure=fig, hspace=0.4)
        text_color = "#e0e0e0"
        accent = "#00d4ff"

        fig.suptitle(
            f"Gravitational Wave Event: {event_name}  •  Detector: {detector}",
            color=accent, fontsize=15, fontweight="bold", y=0.97
        )

        # ── Panel 1: Raw Strain ───────────────────────────────────────────────
        ax1 = fig.add_subplot(gs[0])
        t0 = strain_raw.t0.value
        times_raw = t0 + np.arange(len(strain_raw)) * strain_raw.dt.value - gps
        ax1.plot(times_raw, strain_raw.value, color="#555555", lw=0.5, alpha=0.7)
        ax1.set_ylabel("Strain (raw)", color=text_color, fontsize=9)
        ax1.set_xlabel("Time relative to merger [s]", color=text_color, fontsize=9)
        ax1.axvline(0, color=accent, lw=1.2, linestyle="--", label="Merger")
        ax1.set_facecolor("#111111")
        ax1.tick_params(colors=text_color)
        ax1.legend(fontsize=8, labelcolor=text_color, facecolor="#1a1a1a")
        ax1.set_xlim(-SEGMENT_DURATION / 2, SEGMENT_DURATION / 2)

        # ── Panel 2: Filtered Strain ──────────────────────────────────────────
        ax2 = fig.add_subplot(gs[1])
        times_filt = (
            strain_filtered.t0.value
            + np.arange(len(strain_filtered)) * strain_filtered.dt.value
            - gps
        )
        ax2.plot(times_filt, strain_filtered.value, color="#00d4ff", lw=0.7)
        ax2.axvline(0, color="#ff6b6b", lw=1.2, linestyle="--", label="Merger")
        ax2.set_ylabel(f"Whitened Strain\n({BANDPASS_LOW}–{BANDPASS_HIGH} Hz)", color=text_color, fontsize=9)
        ax2.set_xlabel("Time relative to merger [s]", color=text_color, fontsize=9)
        ax2.set_facecolor("#111111")
        ax2.tick_params(colors=text_color)
        ax2.legend(fontsize=8, labelcolor=text_color, facecolor="#1a1a1a")
        ax2.set_xlim(-2, 1)

        # ── Panel 3: Q-Transform Spectrogram ─────────────────────────────────
        ax3 = fig.add_subplot(gs[2])
        plot = q_gram.plot(ax=ax3, figsize=None)
        ax3.set_ylabel("Frequency [Hz]", color=text_color, fontsize=9)
        ax3.set_xlabel("Time [GPS]", color=text_color, fontsize=9)
        ax3.set_facecolor("#111111")
        ax3.tick_params(colors=text_color)
        ax3.set_yscale("log")
        ax3.set_title("Q-Transform (Chirp Signature)", color=text_color, fontsize=9)

        for ax in [ax1, ax2, ax3]:
            for spine in ax.spines.values():
                spine.set_edgecolor("#333333")

        out_path = self.output_dir / f"{event_name}_{detector}_analysis.png"
        plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close(fig)
        print(f"   📊 Plot saved: {out_path}")

    # ── Report ────────────────────────────────────────────────────────────────

    def _save_report(self, result: AnalysisResult):
        """Save JSON + human-readable text report."""
        # JSON
        json_path = self.output_dir / f"{result.event.name}_{result.detector}_summary.json"
        with open(json_path, "w") as f:
            json.dump(asdict(result), f, indent=2, default=str)
        print(f"   📄 JSON report: {json_path}")

        # Text
        txt_path = self.output_dir / f"{result.event.name}_{result.detector}_report.txt"
        with open(txt_path, "w") as f:
            e = result.event
            f.write(f"{'='*60}\n")
            f.write(f"GRAVITATIONAL WAVE EVENT ANALYSIS REPORT\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"Event:            {e.name}\n")
            f.write(f"Catalog:          {e.catalog}\n")
            f.write(f"Detector:         {result.detector}\n")
            f.write(f"GPS Time:         {e.gps_time}\n")
            f.write(f"Merger Type:      {e.merger_type}\n")
            f.write(f"\n--- Source Properties ---\n")
            if e.mass1:
                f.write(f"Primary Mass:     {e.mass1:.1f} M☉\n")
            if e.mass2:
                f.write(f"Secondary Mass:   {e.mass2:.1f} M☉\n")
            if e.chirp_mass:
                f.write(f"Chirp Mass:       {e.chirp_mass:.1f} M☉\n")
            if e.luminosity_distance_mpc:
                f.write(f"Distance:         {e.luminosity_distance_mpc:.0f} Mpc\n")
            if e.network_snr:
                f.write(f"Network SNR:      {e.network_snr:.1f}\n")
            f.write(f"\n--- Analysis Results ---\n")
            f.write(f"Estimated SNR:    {result.snr_estimate:.1f}\n")
            f.write(f"Peak Frequency:   {result.peak_freq_hz:.1f} Hz\n")
            f.write(f"Chirp Duration:   {result.chirp_duration_s:.2f} s\n")
            f.write(f"\n--- Data Source ---\n")
            f.write(f"GWOSC: https://gwosc.org/\n")
            f.write(f"License: CC BY 4.0\n")
            f.write(f"{'='*60}\n")
        print(f"   📝 Text report: {txt_path}")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _classify_merger(m1: Optional[float], m2: Optional[float]) -> str:
    """Classify merger type based on component masses."""
    if m1 is None or m2 is None:
        return "BBH"  # Default assumption for unknown
    is_m1_ns = m1 <= NS_MAX_MASS
    is_m2_ns = m2 <= NS_MAX_MASS
    if is_m1_ns and is_m2_ns:
        return "BNS"
    elif is_m1_ns or is_m2_ns:
        return "NSBH"
    else:
        return "BBH"


def _get_param(params: dict, key: str) -> Optional[float]:
    """Safely extract a median/bestfit parameter value."""
    val = params.get(key)
    if val is None:
        return None
    if isinstance(val, dict):
        return val.get("best", val.get("median", None))
    return float(val)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Gravitational Wave Event Analyzer — powered by GWOSC public data"
    )
    parser.add_argument("--event", type=str, help="Event name (e.g. GW150914, GW231123_135430)")
    parser.add_argument("--detector", type=str, default="H1", choices=DETECTORS, help="Detector (default: H1)")
    parser.add_argument("--output", type=str, default="./output", help="Output directory")
    parser.add_argument("--list-events", action="store_true", help="List top events from catalog")
    parser.add_argument("--catalog", type=str, default="GWTC-3", choices=CATALOGS, help="Catalog name")
    parser.add_argument("--top", type=int, default=10, help="Number of events to list")
    args = parser.parse_args()

    analyzer = GWEventAnalyzer(output_dir=args.output)

    if args.list_events:
        analyzer.list_events(catalog=args.catalog, top=args.top)
    elif args.event:
        result = analyzer.analyze_event(
            event_name=args.event,
            detector=args.detector,
        )
        print(f"\n{'─'*50}")
        print(f"  Event:        {result.event.name}")
        print(f"  Type:         {result.event.merger_type}")
        print(f"  Detector SNR: {result.snr_estimate:.1f}")
        print(f"  Peak freq:    {result.peak_freq_hz:.1f} Hz")
        print(f"  Output dir:   {result.output_dir}")
        print(f"{'─'*50}\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
