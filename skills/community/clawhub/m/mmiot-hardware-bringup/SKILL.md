---
name: "mmiot-hardware-bringup"
description: "mm-iot-sdk porting guide + hardware debugging: project structure, PA→scan→iperf tiers, SPI/SDIO HAL, and real-silicon bug patterns."
---

# mm-iot-sdk hardware bring-up

This skill covers two distinct but overlapping needs:

1. **Starting a new port** — how to structure the project, which components to implement and
   in which order, what hardware you need, and how to use the tiered example applications
   (porting_assistant → scan → iperf) to prove correctness at each stage.
2. **Debugging a failing port on real hardware** — the specific recurring bug species that only
   manifest on silicon, and the GDB-driven methodology for finding them quickly.

Read the whole skill before diving in. The porting structure sections tell you *what* to build;
the debugging sections tell you *why it doesn't work yet* and how to find out for certain.

---

## 0. Before you start: do you actually need a custom port?

Morse Micro ships ready-made platform ports for **Zephyr, ESP32, and CMSIS**. If your host
platform is one of these (or can target one of these ecosystems), use the existing port rather
than writing a new one from scratch — see the *MCU Platform Ports* section of the mm-iot-sdk
documentation.

For bare-metal or FreeRTOS-on-STM32 targets, Morse Micro already ships full reference shims
for four STM32 families. Before writing new shim code, check whether your MCU is close enough
to reuse one directly:

| MCU family    | mm-iot-sdk platform name              |
|---------------|---------------------------------------|
| STM32H753xx   | `mm-ekh08-h753`                       |
| STM32U575xx   | `mm-ekh08-u575`                       |
| STM32U585xx   | `mm-mm6108-ekh05` / `mm-mm8108-ekh05` |
| STM32WB55xx   | `mm-ekh08-wb55`                       |

If none of the above fit, proceed with a custom port. The rest of this skill is that process.

---

## 1. Hardware requirements

Verify these before writing a single line of port code.

### Transport bus

Choose **one** of SPI or SDIO — the SDK does not support sharing the bus with other
peripherals and you implement only one HAL.

**SDIO is generally more straightforward to bring up than SPI** (Morse Micro's own finding):
the SDIO protocol is more complex, but SPI host controller behavior varies widely across
MCU vendors, making SPI shims harder to get right first time.

### GPIO pins

| Pin       | Direction            | Edge / Level | Notes                                                                                |
|-----------|----------------------|--------------|--------------------------------------------------------------------------------------|
| BUSY      | Transceiver → Host   | Rising edge  | Prevents host from sleeping. Configure as input with rising-edge interrupt.          |
| WAKE      | Host → Transceiver   | Output       | Prevents transceiver sleeping. Hold HIGH permanently until power-optimisation phase. |
| RESET_N   | Host → Transceiver   | Active LOW   | LOW resets transceiver (cold boot).                                                  |
| SPI_IRQ   | Transceiver → Host   | Falling edge | **SPI only.** Data-ready signal. Configure as input with falling-edge interrupt.     |
| CSS       | Host → Transceiver   | Output       | **SPI only.** Software chip-select for clock training sequence.                      |

> **Critical:** Even when WAKE is held permanently HIGH, you **must** call
> `mmwlan_set_sleep_mode(MMWLAN_SLEEP_DISABLE)` after booting the transceiver. Omitting
> this call will cause the driver to fail to boot, even though the WAKE line is correct.

### Memory minimums

| Resource | Minimum | Notes                                                                     |
|----------|---------|---------------------------------------------------------------------------|
| Flash    | 2 MB    | Enough for a debug build with firmware + BCF embedded as C arrays.        |
| SRAM     | 256 KB  | For morselib runtime + FreeRTOS + LwIP buffers + mmpktmem packet memory.  |

These are starting-point figures for bring-up. Final product sizing depends on your application;
see Appendix A.5 of APPNOTE-45 for detailed flash and RAM breakdowns.

### Recommended peripherals

- **PKA (public key accelerator):** accelerates ECC for WPA3/SAE association and reduces
  RAM usage during crypto operations.
- **Hardware RNG:** required by mbedTLS.

---

## 2. Recommended project structure

Do **not** place your project inside the mm-iot-sdk directory — it makes version upgrades and
SDK patching fragile and blurs the boundary between your code and Morse Micro's code.

Instead:

```
YOUR_REPOSITORY/
  third_party/
    mm-iot-sdk-<version>/       <- version-controlled copy of the SDK
  your_application/
    Makefile
    include/
    src/
    targets/
      your_port/
        mm_shims/               <- most of your porting work lives here
        bsp/                    <- MCU-specific clock, peripheral, linker config
        platform.mk
```

- Use the `MMIOT_ROOT` environment variable everywhere your build system references SDK
  components. This lets you move or upgrade the SDK without touching every path.
- Keep `mm_shims/` (the morselib HAL implementations) and `bsp/` (MCU board bring-up)
  separate. The shims are portable across boards of the same MCU family; the BSP is not.
- The porting-stubs companion repository (see Appendix A.7 of APPNOTE-45) provides a
  starting skeleton to copy rather than building the stub from scratch.

---

## 3. The porting process: tiered validation

The port is complete when it passes all four tiers. Work through them in order — later tiers
are impossible to diagnose correctly while earlier ones are still broken.

```
Tier 1  porting_assistant  -> OSAL + GPIO + bus HAL + BCF/FW loading verified
Tier 2  scan               -> transceiver boots, UMAC can probe for HaLow APs
Tier 3  iperf              -> full data path, TCP/IP, throughput benchmarked
Tier 4  your application   -> application-specific performance targets met
```

### 3.1 Build integration first

Before implementing anything:

```bash
make -C applications/porting_assistant \
     MMIOT_ROOT=./third_party/mm-iot-sdk-<version>/framework \
     TARGET=targets/your_port
```

Flash the stub and confirm you can get *any* serial output. If the board is silent, the
debug-probe setup or the UART driver is wrong — fix that before going further (see §7.4 below).

To identify exactly which source files, include paths, and build defines an example uses:

```bash
make -C mm-iot-sdk/examples/<example>/targets/<platform> VERBOSE=1
```

Parse the VERBOSE output rather than guessing at file lists.

### 3.2 porting_assistant in four stages

Each stage has a definitive expected serial output. Use the output, not code review, to confirm
a stage is actually passing.

**Stage A — compile and get any output:**

Implement `mmhal_log_write()` first. Provide `ASSERT(false)` stubs for anything else that
fails to link. Expected output: all tests `[ FAIL ]`.

**Stage B — OSAL passes:**

Implement the functions in `mmosal.h` and `mmhal_os.h`. Key functions exercised by the PA:

| PA test                  | Function(s)               |
|--------------------------|---------------------------|
| Memory allocation        | `mmosal_malloc_()`        |
| Memory reallocation      | `mmosal_realloc_()`       |
| Passage of time          | `mmosal_get_time_ms()`    |
| Task creation/preemption | `mmosal_task_create()`    |

If you are using **FreeRTOS**, use the existing `mmosal_shim_freertos.c` from the SDK rather
than writing your own OSAL shim. Confirm your FreeRTOS version matches the SDK's (v11.2).
Not all OSAL functions are exercised by the PA, but all of them must be implemented.

Expected output at end of Stage B: OSAL rows `[ PASS ]`, all others `[ FAIL ]`.

**Stage C — communications HAL passes:**

Implement GPIO manipulation functions first. Test each one individually with a logic analyzer
before touching the bus driver: assert/deassert RESET, WAKE, read BUSY, etc.

Then implement the bus HAL (SPI *or* SDIO — see §4 and §5 for specifics). The PA will run a
bulk write/read and a raw throughput test.

Expected output at end of Stage C: all rows through `Raw throughput test [ PASS ]`,
firmware rows still `[ FAIL ]`.

**Stage D — BCF and firmware:**

Implement `mmhal_wlan_read_fw_file()` and `mmhal_wlan_read_bcf_file()`.

The simplest approach: convert `.mbin` files to C arrays and compile them in:

```bash
xxd -i <file.mbin> | sed 's/unsigned char/const unsigned char/' > <file.c>
```

Alternatively use the linker-object approach with `INCLUDE_BCF_FILE_IN_APPLICATION` (see
`framework/mk/morsefirmware.mk`). See `mmhal_wlan_binaries.c` for a reference implementation.

Expected output: all tests `[ PASS ]`, with a raw throughput line like:
```
Raw TPUT (kbit/s): 24615
```

### 3.3 Benchmark baselines

Use these to sanity-check your SPI/SDIO implementation once the PA passes. A result
significantly below these numbers means your bus HAL or DMA config needs attention *before*
proceeding to scan/iperf.

**porting_assistant raw throughput (kbit/s):**

| Platform                | Time (ms) | Transactions | Bytes      | Raw TPUT |
|-------------------------|-----------|--------------|------------|----------|
| mm-mm6108-ekh05 (SPI)   | 2501      | 2254         | 6,743,968  | 21,572   |
| mm-mm8108-ekh05 (SPI)   | 2501      | 2564         | 7,671,488  | 24,538   |
| mm-mm8108-ekh05 (SDIO)  | 2501      | 11,670       | 34,916,640 | 111,688  |

**iperf end-to-end throughput (Mbps, EKH05 boards):**

| Transceiver | Protocol | UDP DL | UDP UL | TCP DL | TCP UL |
|-------------|----------|--------|--------|--------|--------|
| MM6108      | SPI      | 18.0   | 18.0   | 8.1    | 6.4    |
| MM6108      | SDIO     | 24.0   | 24.0   | 9.5    | 7.0    |
| MM8108      | SPI      | 19.0   | 19.9   | 9.8    | 7.8    |
| MM8108      | SDIO     | 30.0   | 24.9   | 10.5   | 8.5    |

### 3.4 scan

Needs a HaLow AP (e.g. HaLowLink1, EKH01). Compile the same way as porting_assistant,
substituting `applications/scan`. Remove optional components (mmconfig, mbedtls, littlefs)
if you hit build errors — they are not required for scan to work. Set `COUNTRY_CODE` to a
region present in `mmregdb.c`'s `regulatory_db_domains[]`.

Successful output: probe responses with BSSID, RSSI, S1G operation fields printed.

### 3.5 iperf

Configure `iperf/src/mm_app_loadconfig.c` (country code, SSID, passphrase, security type)
and `iperf/src/iperf.c` (server/client mode, duration, port). Needs iPerf v2.x on the AP.

Compare results against the table in §3.3. If you're significantly below reference values,
see §7.7 (throughput troubleshooting) before treating the port as complete.

---

## 4. SPI HAL specifics

Reference shims live at:
`mm-iot-sdk/framework/src/platforms/*/mm_shims/mmhal_wlan.c`

| Parameter         | Requirement                                                                                       |
|-------------------|---------------------------------------------------------------------------------------------------|
| Role              | Host is SPI master; transceiver is slave.                                                         |
| Mode              | Mode 0 only: CPOL=0, CPHA=0.                                                                      |
| Bit order         | MSB first.                                                                                        |
| Frame size        | 8-bit.                                                                                            |
| Duplex            | Half-duplex protocol over full-duplex pins (both MISO and MOSI must be wired).                    |
| Clock frequency   | 20 MHz is a safe starting point; some platforms reach 40 MHz. See transceiver datasheet for max.  |
| Chip select       | Software-controlled GPIO — do not use the SPI peripheral's hardware NSS.                          |
| Training sequence | Host must clock >74 pulses with CS deasserted before the first transaction.                       |
| DMA               | Strongly recommended. Use DMA for transfers >=16 bytes (`DMA_TRANSFER_MIN_LENGTH`); polled below. |
| Buffer alignment  | Bulk read/write buffers passed to `mmhal_wlan_spi_read_buf/write_buf` must be 32-bit aligned.    |
| Transfer timeout  | Block on completion (DMA interrupt or equivalent) with ~10 ms per-transfer timeout.              |
| SPI_IRQ polarity  | **Falling edge.** The transceiver asserts SPI_IRQ low to signal data is ready.                    |

Without DMA, the host will stall the morselib worker thread and throughput will be well below
the reference figures in §3.3.

**SPI debug loopback trick:** Wire MISO directly to MOSI on the bench, then call the read/write
functions and verify the bytes echo back correctly. This confirms your SPI peripheral config and
GPIO chip-select logic before connecting the transceiver.

---

## 5. SDIO HAL specifics

Reference shims live at:
`mm-iot-sdk/framework/src/platforms/*-sdio/mm_shims/mmhal_wlan.c`

| Parameter        | Requirement                                                                                      |
|------------------|--------------------------------------------------------------------------------------------------|
| Role             | Host is SDIO controller; transceiver is SDIO card.                                               |
| Bus width        | 4-bit (enable `ENABLE_SDIO_4BIT`). 1-bit is supported as fallback only.                         |
| Init clock       | 400 kHz during card enumeration (`SD_INIT_FREQ_HZ`).                                            |
| DMA              | Internal DMA (IDMA, single-buffer mode) required. Buffers 32-bit aligned, length multiple of 4. |
| Write timeout    | 750 ms.                                                                                          |
| Read timeout     | 1000 ms.                                                                                         |
| IRQ delivery     | In-band via DAT1 (`SDMMC` peripheral delivers `SDIO_IT_SDIOIT`). No separate IRQ GPIO needed.   |
| BUSY GPIO        | Still required as a separate GPIO even with SDIO — BUSY is not carried in-band.                  |

The transceiver presents two SDIO functions: function 1 (control, 8-byte block size) and
function 2 (data, 512-byte block size). Communication uses CMD52 (single-register) and
CMD53 (block/byte multi-access).

---

## 6. morselib: prebuilt vs. source

You can either compile morselib from source with your application, or link against the
prebuilt `libmorse.a` in `mm-iot-sdk/framework/morselib/lib/`.

The prebuilt is available for:
- `arm-cortex-m33f`
- `arm-cortex-m4f`
- `arm-cortex-m7f`

You **must** use the **NewLib-Nano** C library implementation when linking against the prebuilt.
Your CPU architecture and toolchain flags must exactly match one of the above configurations.
If they don't, compile from source.

---

## 7. Debugging real hardware — the core rule

**Every failure is a real bug until proven otherwise.**

When a test step fails, hangs, or a board comes up silent, resist the urge to treat it as
flaky hardware, a timing fluke, or something to work around. Chase every failure to its actual
root cause before moving on. "Just retry" or "add a delay" almost never finds the real bug;
they hide it.

The one exception: if code has been proven correct by cross-referencing a reference platform
or by other tests on the same signal passing, ask the user to double-check the physical
connection before assuming a software bug (see §7.10 below).

---

## 7.1 Don't trust "should be compatible" — read the real vendor source

New platforms are often built against an MCU family that's "basically the same as" a family
already in the tree (e.g. GD32F4xx vs STM32F4). That similarity is real but incomplete, and
the gaps are exactly where bugs hide:

- If a vendored driver library isn't available yet and code is hand-written from general
  knowledge of a "compatible" family, treat every register name, bit position, and function
  signature as unverified until the real vendor library is dropped in and diffed against.
  Function signatures shift (extra parameter on a PLL-config call), and constants that look
  parallel across families can occupy *different bit positions* in the same register.
- When two constants look like a matched pair (a "config/request" constant and a
  "status/readback" constant), check their actual definitions. A common vendor pattern is to
  have a `_config()` constant and a `_get()`/status constant that are *not* interchangeable
  even though they represent "the same" thing conceptually.
- Cross-validate GPIO/interrupt configuration against a working sibling platform. If the
  sibling configures an edge as rising-only and the new platform uses both edges, that's a
  strong signal of a bug, not an intentional difference.

---

## 7.2 Boot and vector table placement

If the board appears to still be running factory firmware after a successful flash:

- Cortex-M cores fetch the initial stack pointer and reset vector from fixed physical addresses
  at cold reset, independent of VTOR. If the linker script places `.vectors`/`.isr_vector`
  somewhere other than that physical boot address (e.g. assuming a bootloader will jump there)
  and no bootloader exists, the CPU boots whatever was already at address 0 — indefinitely.
- `verify` after programming only checks the bytes it wrote, not whether they're reachable.
- Check `SystemInit()` (or equivalent): some vendor startup code unconditionally forces VTOR
  to a fixed address on every boot.
- A `BOOTLOADER` memory region in a linker script does not guarantee a bootloader is actually
  built and flashed — it may be a reserved placeholder. If so, the fix is placing `.vectors`
  directly in the boot region, not writing a bootloader.

---

## 7.3 Debugging a silent/hanging board with GDB

Don't re-read "correct-looking" init code hoping to spot a bug. Attach GDB and find out where
execution actually is:

1. `openocd -f <platform's openocd.cfg>` in one terminal, `arm-none-eabi-gdb <elf>` in
   another, `target extended-remote :3333`.
2. `monitor reset halt`, `load` (if needed), `continue`. If it hangs, `Ctrl-C` then `bt`.
3. If the backtrace lands in a generic fault/error handler called from multiple sites (very
   common for `SystemClock_Config()`-style functions with several `if (...) Error_Handler()`
   checks), `disassemble` the calling function, find each call site address, and set
   breakpoints at each to identify which specific check failed. Don't assume the first failing
   check in source order is the one that fired.
4. Prefer this over speculative code changes. A five-minute GDB session that shows "this
   readback returned 8, code expected 2" is worth more than three guesses at a fix.

---

## 7.4 Silent serial output — check the probe first

Before chasing a UART driver bug:

- Confirm the debug-probe config isn't a leftover placeholder (e.g. J-Link config when the
  board ships with a CMSIS-DAP probe). Set an explicit target chip name if the config relies
  on auto-detection.
- If the probe is a separate dongle, its UART header may be an independent USB-to-serial
  bridge with no built-in connection to the target. "No serial output" can simply mean the
  probe's TX/RX header was never jumpered to the target MCU's UART pins.
- If flashing tooling auto-detects the platform via OpenOCD target name, make sure the new
  platform is registered in that lookup table — a missing entry looks like flash corruption
  but is really just a missing config registration.

---

## 7.5 Transceiver fails to boot (SPI_IRQ)

**Symptom:** `mmwlan_boot()` returns `MMWLAN_ERROR`.

**Cause:** SPI_IRQ not implemented correctly. The transceiver uses the SPI_IRQ line (falling
edge) to signal that data is ready for the host to read. If the interrupt is not wired up and
calling the registered handler, the transceiver cannot complete boot.

**Fix:** Verify SPI_IRQ is configured as a falling-edge input interrupt and that
`mmhal_wlan_register_spi_irq_handler()` / `mmhal_wlan_set_spi_irq_enabled()` are correctly
implemented. Check with a logic analyzer that the line actually toggles during boot.

---

## 7.6 Flash / config-store address bugs

Code that maps a flash address to "which erasable sector is this" often uses bare equality
checks (`address == sector_start`) rather than range containment checks
(`start <= address < start + size`). The equality form silently returns "not found" for any
address that falls *within* a sector without being its first byte.

This manifests as a config-store or filesystem failure deep inside a generic storage library —
a confusing "can't find valid partition" or assertion that looks like flash corruption but is
actually a HAL bug one level below. When you see an address-to-sector/block lookup, verify it
does a real range check and test it against both the first and last byte of a region.

---

## 7.7 Lower than expected throughput

**Symptoms:** Raw TPUT in porting_assistant significantly below §3.3 baselines, or iperf
results far below the reference table.

**Common causes and fixes:**

1. **No DMA, or DMA misconfigured.** The reference shims use DMA for transfers >=16 bytes and
   fall back to polled for smaller transfers. Without DMA the morselib worker thread stalls.
   Check DMA is enabled and that the channel/stream config is correct.

2. **DMA access width mismatch.** If `mmpktmem` buffers were moved to a different SRAM region
   (e.g. from default SRAM to a larger DTCM), check that the DMA controller is configured for
   32-bit access to the new region. The 8-bit config may have worked for the original SRAM type
   but silently degrades throughput on the new one — a known real bug on an existing port.

3. **Code executing from XIP flash.** If the linker places code in QSPI execute-in-place flash
   rather than internal SRAM, the QSPI bus becomes a bottleneck. Check whether the platform
   vendor provides an alternate linker definition to copy code to RAM at boot.

4. **Interrupt handlers not returning quickly.** Keep ISRs minimal; defer work to tasks via
   queues or semaphores.

5. **Insufficient packet memory.** Ensure `mmpktmem` allocation is sized correctly for your
   network stack buffer requirements (LwIP uses pbufs).

To diagnose: capture a logic-analyzer trace of the bus and look for large idle gaps or
inconsistent clock behaviour.

---

## 7.8 GPIO/EXTI "looks parallel, isn't" configuration

Interrupt trigger-edge configuration is an easy place to introduce a doubling bug: configuring
"both edges" when only one is semantically meaningful (e.g. BUSY where only the *asserting*
edge should trigger) causes every toggle to fire the handler twice. This surfaces as a test
that counts interrupt invocations getting exactly 2x the expected count — a strong signal to
check the trigger type, not the counting logic.

For SPI_IRQ specifically: the edge is **falling** (transceiver asserts low). For BUSY: the
edge is **rising**. Getting these reversed produces spurious or missing interrupts that are
extremely hard to trace without a logic analyzer.

Whenever you write or review edge-trigger configuration, add a comment stating which specific
edge matters and why, and verify the code matches the comment.

---

## 7.9 HostAP multiple-definition linker errors

**Symptom:** Multiple definition linker errors on HostAP symbols.

**Cause:** Your project already includes HostAP (e.g. for a 2.4 GHz interface) and morselib
brings in its own modified version.

**Fix:** Name-mangle the Morse Micro HostAP and all references to it in morselib. See
Appendix A.6 of APPNOTE-45 for the procedure.

---

## 7.10 Distinguish software bugs from wiring bugs

Make the call based on evidence, not a guess:

- If a companion chip's SPI/register communication has already passed other tests (clock, data,
  and chip-select demonstrably working), and only one specific signal fails, and that signal's
  software-side mapping is shared/chip-agnostic code already used identically by other working
  platforms, the software is unlikely to be the problem — say so and ask the user to physically
  check that specific connection.
- Don't reach for "probably miswired" as a first resort. Only do so after you've ruled out the
  software path via the reasoning above or via GDB/register inspection.

---

## 8. Document every finding immediately

Each confirmed hardware-only bug is expensive to rediscover. For every confirmed bug:

1. Fix it with a comment at the fix site explaining *why* the old code was wrong — include
   specific evidence (GDB register values, the failing address) so the reasoning is
   reconstructable later.
2. Add an entry to the platform's provenance/history doc describing symptom, root cause, and
   fix in enough detail for a future porter to pattern-match against it on a different platform.
3. Keep the platform's README "read this before using on real hardware" section current with
   a count and one-line summary of confirmed bugs, so a new user knows what's been shaken out.

---

## 9. Quick checklist for a fresh bring-up session

Work through these in order. Later categories only surface once earlier ones are fixed.

1. **Pre-port:** Zephyr/ESP32/CMSIS port or STM32 reference shim covers the target? Use it.
2. **Hardware verified:** >=2 MB flash, >=256 KB SRAM, SPI or SDIO wired, GPIO pins correct.
3. **Project structure:** mm-iot-sdk in `third_party/`, `MMIOT_ROOT` used, `mm_shims/` and `bsp/` separate.
4. **Debug probe:** config matches actual hardware (probe type, chip name, UART wiring to target).
5. **Board boots new firmware:** vector table lands at the real boot address; not still running factory firmware.
6. **PA Stage B — OSAL passes:** memory alloc, time, task preemption all `[ PASS ]`.
7. **PA Stage C — bus HAL passes:** SPI/SDIO startup, chip ID, BUSY, bulk R/W, raw TPUT all `[ PASS ]`; raw TPUT within ~20% of reference baselines in §3.3.
8. **PA Stage D — BCF/FW passes:** all PA tests `[ PASS ]`.
9. **scan passes:** transceiver boots, probe responses appear.
10. **iperf passes:** end-to-end data path verified, throughput benchmarked against §3.3 table.
11. **Only after 1-10** are solid: debug application-level / protocol-level behaviour. Failures there are much harder to diagnose correctly while a lower-level bug still lurks underneath.

---

## 10. Component dependency reference

When assembling your build, use this dependency table to avoid missing includes:

| Component  | Depends on                                                                   |
|------------|------------------------------------------------------------------------------|
| `morselib` | HostAP                                                                       |
| `mmutils`  | morselib                                                                     |
| `mmpktmem` | morselib, mmutils                                                            |
| `mmconfig` | morselib                                                                     |
| `mmregdb`  | morselib                                                                     |
| `mmipal`   | lwip, morselib, mmutils (`IP_STACK=lwip` required)                           |
| `mmiperf`  | lwip, morselib, mmutils (`IP_STACK=lwip` required)                           |
| `mmping`   | lwip, morselib, mmutils (`IP_STACK` required)                                |
| `lwip`     | mbedTLS (only when `altcp_tls_mbedtls.c` is compiled)                       |
| `mbedtls`  | lwip (via `net_lwip.c`, only when `IP_STACK` set), morselib                 |
| `hostap`   | morselib (`os_mmosal.c`, `morse_stubs.c`); mbedTLS (`crypto_mbedtls_mm.c`) |

`mmconfig`, `mbedtls`, and `littlefs` are **optional** for the scan and iperf examples and can
be removed from the build without affecting their main functionality if they cause build issues.
