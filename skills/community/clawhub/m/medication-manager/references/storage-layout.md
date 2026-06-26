# Storage Layout

This skill uses a **file-based** storage system. No database required — just markdown files.

## Directory Structure

```
data/
├── medications/               # One .md file per medication
│   ├── 阿莫西林.md
│   ├── 布洛芬.md
│   ├── 蒙脱石散.md
│   └── ...
├── members/                   # One .md file per family member
│   ├── 张三.md
│   ├── 李四.md
│   └── ...
├── prescriptions/             # Prescription records (optional)
│   ├── 2026-04-13_市人民医院.md
│   └── ...
├── logs/                      # Daily medication intake logs
│   ├── 2026-04-13.md
│   ├── 2026-04-14.md
│   └── ...
└── media/                     # Photos of prescriptions/medicine boxes
    └── YYYY-MM-DD/
        ├── prescription_001.jpg
        ├── medicine_box_002.png
        └── ...
```

## Naming Conventions

### Medication Files
- **Filename**: `{通用名}.md` (e.g., `阿莫西林.md`, `布洛芬.md`)
- If multiple brands of the same drug, use generic name in filename
- Include brand name as a field inside the file

### Member Files
- **Filename**: `{姓名}.md`
- Include birth date, weight, allergies, chronic conditions

### Prescription Files
- **Filename**: `{日期}_{医院或科室}.md`
- Include diagnosis, prescribed medications, doctor name

### Log Files
- **Filename**: `YYYY-MM-DD.md`
- One file per day, append entries as medications are taken

### Media Files
- **Folder**: `YYYY-MM-DD/` (date of photo)
- **Filename**: `{type}_{sequence}.{ext}` (e.g., `prescription_001.jpg`)

## Medication File Format

Each medication file follows this structure:

```markdown
# {通用名} ({商品名})

## Basic Info
| Field | Value |
|-------|-------|
| Generic Name | {通用名} |
| Brand Name | {商品名} |
| Specification | {规格} |
| Manufacturer | {生产厂家} |
| Approval No | {批准文号} |
| Drug Type | 处方药 / OTC / 外用药 |
| Category | 抗生素 / 感冒药 / etc. |
| Indications | {适应症} |
| Contraindications | {禁忌} |
| Storage | {储存条件} |

## Batches
| Batch No | Mfg Date | Expiry | Qty | Unit | Location | Status |
|----------|----------|--------|-----|------|----------|--------|
| {批号} | {date} | {date} | {n} | 盒 | {位置} | active |

## Usage Notes
- Adult dose: ...
- Child dose: ...
- Food: before/after meals
- Special: {warnings}

## History
| Date | Member | Action | Notes |
|------|--------|--------|-------|
```

## Finding Medications

### Search by name
Scan filenames in `data/medications/` — filenames are the generic name.

### Search by batch/expiry
Scan the "Batches" table in each medication file for expiry dates.

### Search by category
Scan the "Drug Type" or "Category" field in each file.

### Search by member
Check the "History" table in each medication file, or check the member's file for "Current Medications".

## Storage Tips

1. **Keep files small**: Each medication is one file; don't split batches across files
2. **Use tables**: Markdown tables are easy to read and parse
3. **Consistent dates**: Always use `YYYY-MM-DD` format
4. **Status tracking**: Use `active`, `expired`, `depleted`, `discarded` for batch status
5. **Backup**: The entire `data/` directory is your database — back it up regularly
