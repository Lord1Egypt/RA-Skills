# Credential

Global服务和Region级服务的credentials构建方式不同

```python
from huaweicloudsdkcore.auth.credentials import BasicCredentials, GlobalCredentials

# Regional services
basic_credentials = BasicCredentials(ak, sk).with_security_token(security_token)

# Global services
global_credentials = GlobalCredentials(ak, sk).with_security_token(security_token)
```


如下服务为global服务: IAM、CONFIG、TMS、EPS、Organization； 其他服务均为region级服务。