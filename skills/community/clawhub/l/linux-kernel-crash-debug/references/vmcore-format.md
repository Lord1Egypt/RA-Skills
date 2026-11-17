# vmcore File Format

Detailed kernel dump file format reference.

> **Sensitive artifact:** A vmcore can contain credentials, encryption keys,
> process memory, hostnames, paths, and customer data. Keep raw dumps and
> derived output access-controlled; do not upload, transmit, or paste them into
> external services without explicit authorization and approved sanitization.

## ELF Format Basics

The kernel's `/proc/vmcore` uses ELF (Executable and Linkable Format). A saved
dump may instead use makedumpfile's kdump-compressed format; identify it before
choosing a parser. The following `readelf` examples require ELF input:

```bash
# Check vmcore type
file vmcore
# Output: ELF 64-bit LSB core file, x86-64, version 1 (SYSV), SVR4-style

# View ELF header
readelf -h vmcore

# View Program Headers (describe memory segments)
readelf -l vmcore

# View Section Headers
readelf -S vmcore

# View Note Sections
readelf -n vmcore

# Use objdump to view
objdump -p vmcore     # Program Headers
objdump -x vmcore     # All header information
```

### ELF Core Dump Structure

```
+------------------+
|   ELF Header     |  <- File type: ET_CORE
+------------------+
| Program Headers  |  <- Describe memory segments
+------------------+
|  Note Sections   |  <- VMCOREINFO, registers, etc.
+------------------+
|   Memory Segments|  <- Actual memory contents
+------------------+
```

## VMCOREINFO

VMCOREINFO is an ELF note containing critical kernel information. Core files
can carry notes through `PT_NOTE` program headers without a section table.

```
# Inspect the notes in an ELF vmcore
readelf -n vmcore | grep -A 100 VMCOREINFO
```

This is an inspection aid, not a complete parser: `readelf` may display a note's
description as hexadecimal bytes, and a fixed context length may truncate it.
Use a format-aware tool to extract and parse the full note within its recorded
size. `crash> sys -i` displays DMI strings, not VMCOREINFO; dereferencing the
character pointer `vmcoreinfo_data` once does not extract the whole note.

### Key Fields

| Field | Description |
|-------|-------------|
| `OSRELEASE` | Kernel version string |
| `PAGESIZE` | Page size |
| `SYMBOL(init_uts_ns)` | Address of the kernel UTS namespace object |
| `NUMBER(phys_base)` | Physical address base (x86_64) |
| `NUMBER(VA_BITS)` | Maximum configured virtual address width (ARM64) |
| `NUMBER(TCR_EL1_T1SZ)` | Runtime TTBR1 size offset; ARM64 width is `64 - T1SZ` |
| `KERNELOFFSET` | Kernel offset (KASLR) |
| `CRASHTIME` | Crash timestamp |

### Structure Information

VMCOREINFO contains sizes and member offsets of key structures:

```
SIZE(page)=64
OFFSET(page.flags)=0
OFFSET(page._refcount)=8
OFFSET(page.mapping)=24

SIZE(pglist_data)=...
SIZE(zone)=...
SIZE(free_area)=...
SIZE(list_head)=16
```

### Symbol Addresses

```
SYMBOL(init_uts_ns)=ffffffff8283a040
SYMBOL(node_online_map)=ffffffff8283e000
SYMBOL(swapper_pg_dir)=ffffffff82800000
SYMBOL(init_task)=ffffffff82812480
```

Field availability and structure offsets depend on the producing kernel;
example values are not a substitute for its actual note and matching build.

## Supported Dump Formats

### 1. ELF Core Dump

Standard ELF format, most universal:

```bash
# Features
- Can be read directly by gdb
- Describes the captured memory segments; filtering or missing pages still matter
- ELF dump output does not use makedumpfile's per-page compression

# Generation method
kdump (default configuration)
makedumpfile -E vmcore vmcore.elf
```

### 2. kdump Compressed

Compressed format, saves space:

```bash
# Features
- Default output format of makedumpfile; compression is selected separately
- Requires crash or makedumpfile to parse
- Supports filtering and compression levels

# Generation method
kdump (compression configuration)
makedumpfile -c -d 31 vmcore vmcore.kdump

```

Upstream makedumpfile rejects `-E` when its input is already kdump-compressed.
Select ELF output when processing the original supported ELF input. A compressed
dump can be re-filtered, but excluded pages cannot be restored by conversion.

### 3. diskdump

Red Hat diskdump format:

```bash
# Features
- Red Hat historical format
- Supports compression
- Requires specific kernel patches

# Identification
crash> sys
DUMPFILE: diskdump
```

### 4. netdump

Red Hat netdump format:

> Network delivery does not make a dump less sensitive. Before enabling remote
> collection, authorize the destination, restrict receiver access, protect the
> transport on the trusted network, and define retention and secure disposal.
> Never send a raw production dump to an unapproved endpoint.

```bash
# Features
- Dump transfer via network
- Used for remote crash collection
- Requires netdump server

# Identification
crash> sys
DUMPFILE: netdump
```

### 5. LKCD

Linux Kernel Crash Dump:

```bash
# Features
- Early Linux dump mechanism
- Segmented storage
- Rarely used now
```

### 6. Raw RAM Dump

Raw memory dump:

```bash
# Upstream syntax: a contiguous file and its verified physical start address
crash vmlinux ddr.bin@0x80000000

# Multiple memory regions
crash vmlinux ddr1.bin@0x80000000 ddr2.bin@0x880000000

# Features
- No ELF header
- Requires specifying physical start address
- Common in embedded systems
```

These addresses are examples, not ARM64 defaults. Verify the capture's segment
map, gaps, tool version and target architecture support. `--ram_start` is not
an upstream crash option; a vendor-specific invocation must stay labeled with
its exact tool/build. This raw-input syntax is an authorized human's offline
reference. Agents must keep using the wrapper's regular-file inputs and must
not bypass it to pass unsupported memory sources or arbitrary options.

## kdump Working Principle

### Normal Kernel vs Capture Kernel

```
+-------------------+     +-------------------+
|   Normal Kernel   |     |  Capture Kernel   |
|   (Production)    |     |   (kdump kernel)  |
+-------------------+     +-------------------+
        |                         |
        | crash/panic             |
        |------------------------>|
        |   kexec fast reboot     |
        |                         |
        |                   generate vmcore
        |                         |
        v                         v
```

### Memory Reservation

```bash
# View kdump reserved memory
cat /sys/kernel/kexec_crash_size

# GRUB configuration
crashkernel=128M@16M      # Fixed location
crashkernel=auto          # Distribution-specific support; not universal upstream syntax
crashkernel=256M,high     # Requires architecture/kernel support and suitable low memory
```

Treat boot-parameter changes as persistent host mutations requiring the exact
host/action authorization and rollback described in the main skill. Use the
distribution-specific setup guide rather than applying these sample sizes.

### Dump Process

```
1. Kernel panic
2. kexec quickly starts capture kernel
3. Capture kernel runs
4. Read memory via /proc/vmcore
5. makedumpfile processes and saves
6. Reboot system
```

## makedumpfile Tool

Process and compress vmcore:

```bash
# Basic usage
makedumpfile vmcore vmcore.filtered

# Compression
makedumpfile -c vmcore vmcore.compressed   # zlib
makedumpfile -l vmcore vmcore.compressed   # lzo
makedumpfile -p vmcore vmcore.compressed   # snappy

# Filtering (-d levels)
# 1: Exclude zero pages
# 2: Exclude cache pages
# 4: Exclude all cache pages
# 8: Exclude user data pages
# 16: Exclude free pages
makedumpfile -d 31 -c vmcore vmcore.small  # Minimize

# Convert to ELF
makedumpfile -E vmcore vmcore.elf

# View the tool version
makedumpfile --version

# Split large files
makedumpfile --split vmcore part1 part2 part3

# Reassemble split files
makedumpfile --reassemble part1 part2 part3 vmcore
```

## vmcore Analysis Tips

### Check vmcore Integrity

```bash
# Use file command
file vmcore

# Extract the advertised release; this does not test a full crash session
crash --osrelease vmcore

# Check VMCOREINFO
readelf -n vmcore | grep VMCOREINFO
```

Format identification and metadata extraction do not prove that all required
pages are present or uncorrupted. Compare recorded checksums and capture size,
then validate the dump with exact matching symbols through the supported path.
`makedumpfile -f` means force overwrite; it is not an information or integrity
check and should not be added to preservation or inspection commands.

### Find Matching vmlinux

```bash
# Extract kernel version from vmcore
strings vmcore | grep "Linux version"
readelf -n vmcore | grep OSRELEASE

# Or in crash
crash --osrelease vmcore
```

A release string alone is not an exact-build match. Preserve and compare build
IDs, kernel package/build provenance, modules and configuration. `strings` may
find incidental or stale text and is not a parser for compressed dump pages.

### Handle Corrupted vmcore

```bash
# Human-only offline recovery reference; reduced initialization and command set
crash --minimal vmlinux vmcore
```

`--minimal` may permit limited extraction from a damaged dump; it does not
repair missing data or establish its reliability. `--no_kallsyms` controls use
of kallsyms-generated module symbols, not dump error checking. Agents must
report unsupported recovery needs instead of bypassing the wrapper.

### Rebuild from Partial Memory

```bash
# Multiple memory regions
crash vmlinux mem1.bin@0x0 mem2.bin@0x100000000

# Optional supplemental map file; matching debug vmlinux is still required
crash System.map vmlinux vmcore
```

The raw segment map must come from the capture. `System.map` cannot reconstruct
missing memory or replace type/debug information. Upstream `-S` takes no
argument and selects `/boot/System.map`; it is not `-S <path>`.

## Debugging Information

### View vmcore Details

```
crash> sys
crash> sys -t           # kernel taint information
crash> sys -i           # DMI data, if present; may include serials and UUIDs
```

The `DATE` field in `sys` provides the recorded system time. Upstream `sys -n`
is not an NMI-information command; inspect the actual panic/log and CPU stacks
for NMI context instead. Do not expose DMI identifiers in external reports.

### Memory Layout

```
crash> kmem -v          # vmalloc region
crash> kmem -n          # memory node information
crash> vtop <addr>      # address translation
```

### CPU State

```
crash> bt -a            # all CPU call stacks
crash> mach             # machine information
crash> set -c <cpu>     # switch CPU context
```

## Primary References

- [crash manual](https://github.com/crash-utility/crash/blob/master/crash.8)
- [crash sys help](https://crash-utility.github.io/help_pages/sys.html)
- [VMCOREINFO](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html)
- [makedumpfile manual source](https://github.com/makedumpfile/makedumpfile/blob/master/makedumpfile.8.in)
- [makedumpfile input/output checks](https://github.com/makedumpfile/makedumpfile/blob/master/makedumpfile.c)
