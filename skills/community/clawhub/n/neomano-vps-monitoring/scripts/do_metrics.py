#!/usr/bin/env python3
"""DigitalOcean droplet metrics (Monitoring API) helper.

Auth: DIGITALOCEAN_TOKEN (Bearer)

Commands:
  droplets
  cpu|memory|disk|bandwidth --droplet <name_or_id> --minutes 60

This prints JSON: { ok, droplet, metric, range, summary, raw }
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.digitalocean.com"


def token() -> str:
    t = (os.environ.get("DIGITALOCEAN_TOKEN") or "").strip()
    if not t:
        raise SystemExit("ERROR: missing DIGITALOCEAN_TOKEN")
    return t


def http_get(path: str, params: dict | None = None) -> dict:
    qs = urllib.parse.urlencode({k: v for k, v in (params or {}).items() if v is not None and v != ""})
    url = f"{API}{path}?{qs}" if qs else f"{API}{path}"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token()}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")


def list_droplets() -> list[dict]:
    droplets = []
    page = 1
    per_page = 200
    while True:
        res = http_get("/v2/droplets", {"page": page, "per_page": per_page})
        chunk = res.get("droplets") or []
        droplets.extend(chunk)
        links = (res.get("links") or {}).get("pages") or {}
        if not links.get("next"):
            break
        page += 1
    return droplets


def resolve_droplet(name_or_id: str) -> dict:
    s = str(name_or_id).strip()
    if s.isdigit():
        did = int(s)
        for d in list_droplets():
            if d.get("id") == did:
                return d
        raise SystemExit(f"ERROR: droplet id not found: {did}")

    candidates = [d for d in list_droplets() if (d.get("name") or "").lower() == s.lower()]
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        raise SystemExit(f"ERROR: multiple droplets named '{s}'. Use droplet id instead.")

    # fallback: partial match
    partial = [d for d in list_droplets() if s.lower() in (d.get("name") or "").lower()]
    if len(partial) == 1:
        return partial[0]
    if len(partial) > 1:
        names = ", ".join([f"{d.get('id')}:{d.get('name')}" for d in partial][:10])
        raise SystemExit(f"ERROR: multiple matches for '{s}': {names}")
    raise SystemExit(f"ERROR: droplet not found: {s}")


def _series_first_last(series: dict):
    vals = series.get("values") or []
    if len(vals) < 2:
        return None
    try:
        first_t, first_v = float(vals[0][0]), float(vals[0][1])
        last_t, last_v = float(vals[-1][0]), float(vals[-1][1])
        return first_t, first_v, last_t, last_v
    except Exception:
        return None


def summarize_prometheus(metric: str, result: dict) -> dict:
    """Summarize DigitalOcean Monitoring responses.

    Notes:
    - CPU endpoint returns cumulative CPU seconds split by mode (idle, user, system...).
      We compute a rough utilization % over the requested window using deltas.
    - Other endpoints often return gauges; we fallback to min/max/avg over all samples.
    """
    series = (result.get("data") or {}).get("result") or []
    if not series:
        return {"count": 0}

    if metric == "cpu":
        # Compute utilization from deltas: used = (total - idle) / total
        total_delta = 0.0
        idle_delta = 0.0
        window_seconds = None
        for s in series:
            fl = _series_first_last(s)
            if not fl:
                continue
            t0, v0, t1, v1 = fl
            delta = max(0.0, v1 - v0)
            total_delta += delta
            mode = (s.get("metric") or {}).get("mode")
            if mode == "idle":
                idle_delta += delta
            if window_seconds is None:
                window_seconds = max(1.0, t1 - t0)
        if total_delta <= 0:
            return {"count": 0}
        used_pct = max(0.0, min(100.0, (total_delta - idle_delta) / total_delta * 100.0))
        return {
            "windowSeconds": window_seconds,
            "totalCpuSecondsDelta": total_delta,
            "idleCpuSecondsDelta": idle_delta,
            "usedPercentApprox": used_pct,
        }

    # Generic gauge-ish summary
    values = []
    for s in series:
        for pair in s.get("values") or []:
            try:
                values.append(float(pair[1]))
            except Exception:
                pass
    if not values:
        return {"count": 0}
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "last": values[-1],
    }


def _first_series(raw: dict) -> dict | None:
    series = (raw.get("data") or {}).get("result") or []
    return series[0] if series else None


def _values_map(raw: dict) -> dict[float, float]:
    """Map timestamp->value from the first series in a Prometheus-style response."""
    s = _first_series(raw) or {}
    out: dict[float, float] = {}
    for t, v in s.get("values") or []:
        try:
            out[float(t)] = float(v)
        except Exception:
            continue
    return out


def _combine_prom_series(raw_a: dict, raw_b: dict, fn) -> dict:
    """Combine two Prometheus matrix responses into a single matrix response.

    Keeps only timestamps that exist in BOTH series (intersection).
    """
    a = _values_map(raw_a)
    b = _values_map(raw_b)
    ts = sorted(set(a.keys()) & set(b.keys()))
    values = []
    for t in ts:
        try:
            values.append([t, str(float(fn(a[t], b[t])))] )
        except Exception:
            continue

    return {
        "status": "success",
        "data": {
            "resultType": "matrix",
            "result": [
                {
                    "metric": {},
                    "values": values,
                }
            ],
        },
    }


def fetch_metric(metric: str, host_id: int, start: int, end: int, *, interface: str | None = None, direction: str | None = None) -> dict:
    path = f"/v2/monitoring/metrics/droplet/{metric}"
    params = {"host_id": host_id, "start": start, "end": end}
    if metric == "bandwidth":
        # DO API requires interface=public|private AND direction=inbound|outbound
        params["interface"] = interface or "public"
        params["direction"] = direction or "inbound"
    return http_get(path, params)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("droplets")

    s = sub.add_parser("summary")
    s.add_argument("--minutes", type=int, default=60)

    for m in ["cpu", "memory", "disk", "bandwidth"]:
        p = sub.add_parser(m)
        p.add_argument("--droplet", required=True, help="droplet name or id")
        p.add_argument("--minutes", type=int, default=60)
        if m == "bandwidth":
            p.add_argument("--interface", default="public", choices=["public", "private"])
            p.add_argument("--direction", default="both", choices=["inbound", "outbound", "both"], help="Bandwidth direction. 'both' sums inbound+outbound.")

    args = ap.parse_args()

    if args.cmd == "droplets":
        ds = list_droplets()
        slim = [{"id": d.get("id"), "name": d.get("name"), "region": (d.get("region") or {}).get("slug"), "status": d.get("status")} for d in ds]
        print(json.dumps({"ok": True, "droplets": slim, "count": len(slim)}, indent=2))
        return 0

    if args.cmd == "summary":
        end = int(time.time())
        start = end - int(args.minutes) * 60
        rows = []
        for d in list_droplets():
            host_id = d.get("id")
            name = d.get("name")
            region = (d.get("region") or {}).get("slug")
            status = d.get("status")
            row = {"id": host_id, "name": name, "region": region, "status": status}
            try:
                cpu_raw = fetch_metric("cpu", host_id, start, end)
                row["cpuUsedPercentApprox"] = summarize_prometheus("cpu", cpu_raw).get("usedPercentApprox")
            except Exception as e:
                row["cpuUsedPercentApprox"] = None
                row["cpuError"] = str(e)
            try:
                avail_raw = fetch_metric("memory_available", host_id, start, end)
                total_raw = fetch_metric("memory_total", host_id, start, end)
                mem_raw = _combine_prom_series(avail_raw, total_raw, lambda avail, total: 0.0 if total <= 0 else (1.0 - (avail / total)) * 100.0)
                mem_sum = summarize_prometheus("memory", mem_raw)
                row["memoryUsedPercent"] = mem_sum.get("last")
            except Exception as e:
                row["memoryUsedPercent"] = None
            rows.append(row)
        print(json.dumps({"ok": True, "minutes": args.minutes, "count": len(rows), "rows": rows}, ensure_ascii=False, indent=2))
        return 0

    droplet = resolve_droplet(args.droplet)
    host_id = droplet.get("id")
    end = int(time.time())
    start = end - int(args.minutes) * 60

    if args.cmd == "memory":
        # Memory usage % = 100 * (1 - memory_available/memory_total)
        avail_raw = fetch_metric("memory_available", host_id, start, end)
        total_raw = fetch_metric("memory_total", host_id, start, end)
        raw = _combine_prom_series(avail_raw, total_raw, lambda avail, total: 0.0 if total <= 0 else (1.0 - (avail / total)) * 100.0)
        summary = summarize_prometheus("memory", raw)
        raw["_sources"] = {"memory_available": avail_raw, "memory_total": total_raw}

    elif args.cmd == "disk":
        # Disk usage % = 100 * (1 - filesystem_free/filesystem_size)
        free_raw = fetch_metric("filesystem_free", host_id, start, end)
        size_raw = fetch_metric("filesystem_size", host_id, start, end)
        raw = _combine_prom_series(free_raw, size_raw, lambda free, size: 0.0 if size <= 0 else (1.0 - (free / size)) * 100.0)
        summary = summarize_prometheus("disk", raw)
        # Attach sources for debugging (kept inside raw)
        raw["_sources"] = {"filesystem_free": free_raw, "filesystem_size": size_raw}

    elif args.cmd == "bandwidth":
        interface = getattr(args, "interface", None)
        direction = getattr(args, "direction", "both")
        if direction == "both":
            in_raw = fetch_metric("bandwidth", host_id, start, end, interface=interface, direction="inbound")
            out_raw = fetch_metric("bandwidth", host_id, start, end, interface=interface, direction="outbound")
            raw = _combine_prom_series(in_raw, out_raw, lambda inbound, outbound: max(0.0, inbound) + max(0.0, outbound))
            raw["_sources"] = {"inbound": in_raw, "outbound": out_raw}
        else:
            raw = fetch_metric("bandwidth", host_id, start, end, interface=interface, direction=direction)
        summary = summarize_prometheus("bandwidth", raw)

    else:
        raw = fetch_metric(args.cmd, host_id, start, end, interface=getattr(args, "interface", None))
        summary = summarize_prometheus(args.cmd, raw)

    out = {
        "ok": True,
        "droplet": {"id": droplet.get("id"), "name": droplet.get("name")},
        "metric": args.cmd,
        "range": {"start": start, "end": end, "minutes": args.minutes},
        "summary": summary,
        "raw": raw,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
