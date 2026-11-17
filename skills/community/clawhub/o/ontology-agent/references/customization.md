> **Bilingual — 中英文皆可适配**  This skill ships both Chinese and English content. The Chinese counterpart of this file is `customization.zh.md`.

# User Customization Mechanism (private overrides, without breaking package integrity)

> Core principle: **the skill package provides the "arsenal"; user changes live only in their own private data, `company-data/<company>/instance.yaml`**.
> No matter how the user renames, adds or removes departments, or assigns genders, the skill package's own files are never touched — integrity is always preserved and it can be upgraded/synced at any time.

## 1. The 24-department library vs the user's actual team

- The skill package ships **24 departments** (`experts-template/department_experts.yaml`): 12 core (default team) + 12 optional.
- On first instantiation the 12 core departments are selected by default; optional departments are activated on demand during onboarding.
- Without "modifying the skill package", the user can rename any of these 24, assign a gender, disable them, or add entirely private departments.

## 2. Four kinds of private overrides (written into instance.yaml)

| Field | Purpose | Affects the skill package? |
|------|---------|---------------------------|
| `department_aliases: {code: new_name}` | Rename a department's display name (e.g. `finance` → `Chief Financial Officer`) | No, this instance only |
| `department_genders: {code: female}` | Assign that department's avatar / tone gender | No, this instance only |
| `disabled_departments: [code]` | Disable a department from the team | No, this instance only |
| `custom_departments: [{code,name,gender,expertise,tools_ref,persona}]` | Add a fully private AI employee | No, this instance only |

> Priority: user private overrides > skill package department library defaults. Merge logic: `scripts/init.py: resolve_departments()`.

## 3. Command-line usage (all stored as private data, zero intrusion into the skill package)

```bash
# List the 24-department library (see what is available)
python scripts/init.py --catalog

# List the departments currently in effect for a company
python scripts/init.py --slug weishu --list-depts

# Rename (private override)
python scripts/init.py --slug weishu --rename finance "Chief Financial Officer"

# Assign gender (avatar / tone only, does not affect capability)
python scripts/init.py --slug weishu --gender sales female

# Disable a department
python scripts/init.py --slug weishu --disable mkt_seo
# Re-enable
python scripts/init.py --slug weishu --enable mkt_seo

# Add a private department (a fully custom AI employee)
python scripts/init.py --slug weishu --add-dept cso \
    --name "Chief Security Officer" --gender male \
    --expertise "security strategy, compliance governance, crisis response" \
    --persona-text "Overall owner of company security and compliance governance, reporting directly to the owner"
```

## 4. How this is presented in the digital company's "proactive onboarding"

During progressive onboarding, the business principal will:
1. Start with the 12 core departments (P0 stage);
2. In the P2/P3 stages **gently propose** a few optional departments (e.g. an e-commerce customer may enable `customer_service` / `csm`), suggesting only 1–2 at a time and allowing the user to skip;
3. Tell the user explicitly: renaming, adding, removing and assigning genders are all possible, and "**these changes live only in your own company data and never modify the skill package itself**" — removing the security concern.

## 5. Relationship with the avatar system

- Each department has a `gender_default` (a sensible default inside the skill package), which can be overridden by `department_genders`.
- Avatar selection logic is in `scripts/avatars.py`: the skill package avatar pool is looked up by `(code, gender)`; private departments without a dedicated avatar fall back to the generic pool.
- After the user assigns a gender, regenerating / syncing the expert package makes the corresponding avatar take effect, while the skill package itself stays unchanged.
