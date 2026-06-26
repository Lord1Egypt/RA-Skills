# Parameters Reference

## Required Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--query` | Enzyme name (UniProt search) | `"imine reductase"` |
| `--fasta` | Input FASTA file | `sequences.fasta` |
| `--output` | Output directory | `./output` |

**Note:** Use either `--query` OR `--fasta`, not both.

---

## Optional Parameters

### Performance
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--threads` | 10 | CPU threads |
| `--bootstrap` | 1000 | Bootstrap replicates (≥1000 recommended) |

### Sequence Filtering
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--identity` | 0.90 | CD-HIT identity threshold (0.80-0.95) |
| `--max-sequences` | 1000 | Max sequences to analyze |

### Quality Control
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--min-length` | 100 | Min sequence length (aa) |
| `--max-length` | 2000 | Max sequence length (aa) |

---

## Examples

### Basic usage
```bash
python3 scripts/run_v2.py --query "lipase" --output ./lipase
```

### High-quality analysis
```bash
python3 scripts/run_v2.py \
  --query "esterase" \
  --output ./esterase \
  --threads 20 \
  --bootstrap 2000 \
  --identity 0.95
```

### From FASTA file
```bash
python3 scripts/run_v2.py \
  --fasta my_sequences.fasta \
  --output ./my_analysis \
  --threads 10
```

---

## Recommended Settings

**For publication:**
- `--bootstrap 1000` (minimum)
- `--identity 0.90` (balance diversity vs redundancy)
- `--threads` = number of CPU cores

**For quick test:**
- `--bootstrap 100`
- `--max-sequences 50`

**For large datasets (>500 sequences):**
- `--threads 20`
- `--bootstrap 1000`
- Consider increasing `--identity` to 0.95
