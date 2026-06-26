# OSS 上传（供 EMO/AA 使用）

本地文件需要先上传 OSS，再把公网 URL 传给 DashScope。

## 环境变量
```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID=xxx
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=xxx
export OSS_BUCKET=your-bucket
export OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
```

## Python 示例

### 公开 Bucket（直接返回公网 URL）
```python
import os
import oss2


def upload_to_oss(local_path: str, oss_key: str) -> str:
    auth = oss2.Auth(
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    )
    bucket_name = os.environ["OSS_BUCKET"]
    endpoint = os.environ.get("OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com")
    bucket = oss2.Bucket(auth, f"https://{endpoint}", bucket_name)
    bucket.put_object_from_file(oss_key, local_path)
    return f"https://{bucket_name}.{endpoint}/{oss_key}"
```

### 私有 Bucket（返回签名 URL，默认有效期 3 天）

```python
import os
import oss2

DEFAULT_EXPIRES = 3 * 24 * 3600  # 3 天，单位秒


def upload_to_oss(local_path: str, oss_key: str, expires: int = DEFAULT_EXPIRES) -> str:
    """
    上传文件到私有 OSS bucket，返回带签名的临时访问 URL。

    Args:
        local_path: 本地文件路径
        oss_key:    OSS 对象 key（如 "avatars/face.jpg"）
        expires:    签名 URL 有效期（秒），默认 3 天

    Returns:
        签名过的公网可访问 URL
    """
    auth = oss2.Auth(
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    )
    bucket_name = os.environ["OSS_BUCKET"]
    endpoint = os.environ.get("OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com")
    bucket = oss2.Bucket(auth, f"https://{endpoint}", bucket_name)

    # 上传文件
    bucket.put_object_from_file(oss_key, local_path)

    # 生成签名 URL（GET 方法，expires 秒后过期）
    signed_url = bucket.sign_url("GET", oss_key, expires)
    return signed_url
```

#### 调用示例
```python
url = upload_to_oss("./face.jpg", "avatars/face.jpg")
# → https://your-bucket.oss-cn-beijing.aliyuncs.com/avatars/face.jpg?OSSAccessKeyId=...&Expires=...&Signature=...

# 自定义过期时间（7 天）
url = upload_to_oss("./speech.mp3", "audio/speech.mp3", expires=7 * 24 * 3600)
```

## 注意
- URL 必须公网可访问（http/https），DashScope 需能直接下载
- 签名 URL 过期时间需要覆盖任务处理时长（EMO 任务一般 2~10 分钟，3 天远超所需）
- 私有 Bucket 必须用签名 URL，**不要**用内网 URL 或 `oss://` 协议传给 DashScope
- 建议为临时素材配置 OSS 生命周期规则自动清理（如 7 天后删除）
- `bucket.sign_url()` 返回 `str`，可直接作为 `image_url` / `audio_url` 参数传入
