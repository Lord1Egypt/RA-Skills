
import audit
import json

info = audit.get_os_info()
print(json.dumps(info, indent=2, default=str))
