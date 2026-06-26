# Tool Setup Guide

## Required Python Packages

These are typically available by default:
- `gzip` (stdlib)
- `json` (stdlib)
- `collections` (stdlib)

For report generation:
- `openpyxl` — Excel spreadsheet creation (install with `pip install openpyxl --break-system-packages`)

## samtools / bcftools (for CRAM/BAM analysis)

In sandboxed environments without root access, compile from source:

### Download and Compile samtools

```bash
TOOLS_DIR="$PWD/tools"
mkdir -p "$TOOLS_DIR/bin"

# samtools
cd /tmp
curl -L -o samtools-1.21.tar.bz2 https://github.com/samtools/samtools/releases/download/1.21/samtools-1.21.tar.bz2
tar xjf samtools-1.21.tar.bz2
cd samtools-1.21
./configure --prefix="$TOOLS_DIR" --disable-bz2 --disable-lzma
make -j$(nproc) && make install

# bcftools
cd /tmp
curl -L -o bcftools-1.21.tar.bz2 https://github.com/samtools/bcftools/releases/download/1.21/bcftools-1.21.tar.bz2
tar xjf bcftools-1.21.tar.bz2
cd bcftools-1.21
./configure --prefix="$TOOLS_DIR" --disable-bz2 --disable-lzma
make -j$(nproc) && make install
```

### Key Flags
- `--disable-bz2` and `--disable-lzma`: needed when libbz2-dev / liblzma-dev are not available
- The compiled binaries will be at `$TOOLS_DIR/bin/samtools` and `$TOOLS_DIR/bin/bcftools`

### Verify Installation
```bash
$TOOLS_DIR/bin/samtools --version
$TOOLS_DIR/bin/bcftools --version
```

## Common Issues

### CRAM reference genome
CRAM files need the reference genome. If not available locally, set:
```bash
export REF_PATH=http://www.ebi.ac.uk/ena/cram/md5/%s
```
samtools will auto-fetch reference sequences as needed (requires internet).

### Large file handling
- VCF.gz files: always use `gzip.open()` in Python, or `bcftools view` from command line
- CRAM files: can be 15-30 GB, never load into memory; use `samtools view -r region` for targeted access
- WeGene/23andMe files: small enough (~50MB) to load entirely into a dict
