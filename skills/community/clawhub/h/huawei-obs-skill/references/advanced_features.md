# 高级功能指南

## 断点续传
使用断点续传上传大文件，可以在网络中断后从断点处继续上传：

```python
def resumable_upload(obs_client, bucket_name, object_key, local_file_path, part_size=10*1024*1024):
    """
    断点续传上传文件
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_key: OBS 中的对象路径
        local_file_path: 本地文件路径
        part_size: 分片大小，默认 10MB
        
    Returns:
        bool: 上传是否成功
    """
    try:
        # 断点续传上传
        resp = obs_client.uploadFile(
            bucket_name,
            object_key,
            local_file_path,
            part_size=part_size,
            task_num=5,  # 并发上传的分片数
            enable_checkpoint=True,  # 开启断点续传
            checkpoint_file=f"{local_file_path}.obs_checkpoint"  # 断点信息保存文件
        )
        
        if resp.status < 300:
            print(f"断点续传上传成功: {object_key}")
            # 删除断点文件
            import os
            if os.path.exists(f"{local_file_path}.obs_checkpoint"):
                os.remove(f"{local_file_path}.obs_checkpoint")
            return True
        else:
            print(f"断点续传上传失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"断点续传异常: {e}")
        return False
```

## 文件夹上传
```python
import os

def upload_folder(obs_client, bucket_name, local_folder_path, obs_prefix=''):
    """
    上传整个文件夹到 OBS
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        local_folder_path: 本地文件夹路径
        obs_prefix: OBS 中的路径前缀
        
    Returns:
        dict: 上传结果统计
    """
    success_count = 0
    fail_count = 0
    total_files = 0
    
    # 遍历文件夹
    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            total_files += 1
            local_file_path = os.path.join(root, file)
            # 计算相对路径作为 OBS 中的 key
            relative_path = os.path.relpath(local_file_path, local_folder_path)
            object_key = os.path.join(obs_prefix, relative_path).replace('\\', '/')
            
            print(f"正在上传: {local_file_path} -> {object_key}")
            if upload_file(obs_client, bucket_name, object_key, local_file_path):
                success_count += 1
            else:
                fail_count += 1
    
    print(f"文件夹上传完成: 总文件数 {total_files}, 成功 {success_count}, 失败 {fail_count}")
    return {
        'total': total_files,
        'success': success_count,
        'failed': fail_count
    }
```

## 文件夹下载
```python
def download_folder(obs_client, bucket_name, obs_prefix, local_folder_path):
    """
    下载 OBS 中的整个文件夹到本地
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        obs_prefix: OBS 中的路径前缀
        local_folder_path: 本地保存文件夹路径
        
    Returns:
        dict: 下载结果统计
    """
    # 确保本地文件夹存在
    os.makedirs(local_folder_path, exist_ok=True)
    
    # 列举所有对象
    objects = list_objects(obs_client, bucket_name, prefix=obs_prefix)
    
    success_count = 0
    fail_count = 0
    
    for obj in objects:
        object_key = obj['key']
        # 计算本地文件路径
        relative_path = object_key[len(obs_prefix):] if object_key.startswith(obs_prefix) else object_key
        relative_path = relative_path.lstrip('/')
        local_file_path = os.path.join(local_folder_path, relative_path)
        
        # 确保本地目录存在
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        
        print(f"正在下载: {object_key} -> {local_file_path}")
        if download_file(obs_client, bucket_name, object_key, local_file_path):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"文件夹下载完成: 总文件数 {len(objects)}, 成功 {success_count}, 失败 {fail_count}")
    return {
        'total': len(objects),
        'success': success_count,
        'failed': fail_count
    }
```

## 服务器端加密
```python
from obs import SseKms, SseC

def upload_with_sse_kms(obs_client, bucket_name, object_key, local_file_path, kms_key_id=None):
    """
    使用 SSE-KMS 服务器端加密上传文件
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_key: OBS 中的对象路径
        local_file_path: 本地文件路径
        kms_key_id: KMS 密钥 ID，不指定则使用默认密钥
        
    Returns:
        bool: 上传是否成功
    """
    try:
        sse_header = SseKms()
        if kms_key_id:
            sse_header.kms_key_id = kms_key_id
            
        resp = obs_client.putFile(
            bucket_name, 
            object_key, 
            local_file_path,
            sseHeader=sse_header
        )
        
        if resp.status < 300:
            print(f"加密上传成功: {object_key}")
            return True
        else:
            print(f"加密上传失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"加密上传异常: {e}")
        return False

def upload_with_sse_c(obs_client, bucket_name, object_key, local_file_path, sse_c_key):
    """
    使用 SSE-C 服务器端加密上传文件（客户提供密钥）
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_key: OBS 中的对象路径
        local_file_path: 本地文件路径
        sse_c_key: 256位加密密钥
        
    Returns:
        bool: 上传是否成功
    """
    try:
        sse_header = SseC()
        sse_header.sse_c_key = sse_c_key
        sse_header.sse_c_key_md5 = obs_client.base64_md5(sse_c_key)
        sse_header.sse_c_algorithm = 'AES256'
            
        resp = obs_client.putFile(
            bucket_name, 
            object_key, 
            local_file_path,
            sseHeader=sse_header
        )
        
        if resp.status < 300:
            print(f"SSE-C 加密上传成功: {object_key}")
            return True
        else:
            print(f"SSE-C 加密上传失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"SSE-C 加密上传异常: {e}")
        return False
```

## 生命周期配置
```python
from obs import Lifecycle, Rule, Transition, Expiration

def set_bucket_lifecycle(obs_client, bucket_name):
    """
    设置存储桶生命周期规则
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        
    Returns:
        bool: 设置是否成功
    """
    try:
        # 创建生命周期规则
        lifecycle = Lifecycle()
        
        # 规则1：30天后转为低频访问存储，180天后归档，365天后删除
        rule1 = Rule()
        rule1.id = 'archive_rule'
        rule1.prefix = 'logs/'  # 只对 logs/ 前缀生效
        rule1.status = 'Enabled'
        
        # 30天后转为低频访问
        transition1 = Transition()
        transition1.days = 30
        transition1.storageClass = 'WARM'  # 低频访问存储
        rule1.transition = transition1
        
        # 180天后转为归档存储
        transition2 = Transition()
        transition2.days = 180
        transition2.storageClass = 'COLD'  # 归档存储
        rule1.noncurrentVersionTransition = transition2
        
        # 365天后删除
        expiration = Expiration()
        expiration.days = 365
        rule1.expiration = expiration
        
        lifecycle.rule = [rule1]
        
        resp = obs_client.setBucketLifecycle(bucket_name, lifecycle)
        if resp.status < 300:
            print(f"存储桶生命周期规则设置成功")
            return True
        else:
            print(f"设置生命周期规则失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"设置生命周期规则异常: {e}")
        return False
```

## CORS 配置
```python
from obs import CorsRule

def set_bucket_cors(obs_client, bucket_name):
    """
    设置存储桶 CORS（跨域资源共享）规则
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        
    Returns:
        bool: 设置是否成功
    """
    try:
        cors_rule1 = CorsRule()
        cors_rule1.allowedOrigin = ['*']  # 允许所有来源，生产环境建议设置具体域名
        cors_rule1.allowedMethod = ['GET', 'PUT', 'POST', 'DELETE', 'HEAD']
        cors_rule1.allowedHeader = ['*']
        cors_rule1.maxAgeSeconds = 3600  # 预检请求缓存时间
        cors_rule1.exposeHeader = ['ETag']
        
        resp = obs_client.setBucketCors(bucket_name, [cors_rule1])
        if resp.status < 300:
            print(f"存储桶 CORS 规则设置成功")
            return True
        else:
            print(f"设置 CORS 规则失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"设置 CORS 规则异常: {e}")
        return False
```

## 版本控制
```python
def enable_bucket_versioning(obs_client, bucket_name):
    """
    开启存储桶版本控制
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        
    Returns:
        bool: 设置是否成功
    """
    try:
        resp = obs_client.setBucketVersioning(bucket_name, 'Enabled')
        if resp.status < 300:
            print(f"存储桶版本控制已开启")
            return True
        else:
            print(f"开启版本控制失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"开启版本控制异常: {e}")
        return False
```
