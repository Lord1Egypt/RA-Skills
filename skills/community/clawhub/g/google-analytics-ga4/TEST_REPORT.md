# Skill test checklist

Use this as a manual checklist after configuring credentials. **Do not paste real property IDs or metrics into shared repos.**

1. `pip install -r requirements.txt`  
2. `python test_connection.py --property-id YOUR-PROPERTY-ID`  
3. `python ga_query.py --action realtime --property-id YOUR-PROPERTY-ID`  
4. `python ga_query.py --action historical --property-id YOUR-PROPERTY-ID --start-date yesterday --end-date yesterday`  

If any step fails, see [SKILL.md](SKILL.md) (permissions, API enablement, key path).
