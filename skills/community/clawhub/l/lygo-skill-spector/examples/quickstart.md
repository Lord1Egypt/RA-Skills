# SkillSpector quickstart

```bash
python scripts/self_check.py
python scripts/skill_spector.py scan path/to/any-skill
python scripts/skill_spector.py gate path/to/any-skill --max-band low
python scripts/skill_spector.py batch path/to/skills-root
python scripts/skill_spector.py report path/to/any-skill
```

Exit `10` → treat as high risk. Exit `0` → still read the code for critical paths.

**Full stack builder:** https://chatagent.ca/lygoskillhub.html#full-lygo  
(`builder/skill_spector_builder.py` for HTML multi-root reports)
