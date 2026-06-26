# 对象操作指南

## 上传文件
```python
def upload_file(obs_client, bucket_name, object_key, local_file_path):
    """
    上传单个文件到 OBS
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_key: OBS 中的对象路径
        local_file_path: 本地文件路径
        
    Returns:
        bool: 上传是否成功
    """
    try:
        resp = obs_client.putFile(bucket_name, object_key, local_file_path)
        if resp.status < 300:
            print(f"文件上传成功: {object_key}")
            return True
        else:
            print(f"文件上传失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"上传文件异常: {e}")
        return False
```

## 流式上传大文件
```python
def upload_large_file(obs_client, bucket_name, object_key, local_file_path, part_size=5*1024*1024):
    """
    分片上传大文件（断点续传）
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_key: OBS 中的对象路径
        local_file_path: 本地文件路径
        part_size: 分片大小，默认 5MB
        
    Returns:
        bool: 上传是否成功
    """
    try:
        # 初始化分片上传任务
        resp = obs_client.initiateMultipartUpload(bucket_name, object_key)
        if resp.status >= 300:
            print(f"初始化分片上传失败: {resp.errorMessage}")
            return False
        
        upload_id = resp.body.uploadId
        parts = []
        part_number = 1
        
        import os
        file_size = os.path.getsize(local_file_path)
        
        with open(local_file_path, 'rb') as f:
            while True:
                data = f.read(part_size)
                if not data:
                    break
                    
                # 上传分片
                resp = obs_client.uploadPart(
                    bucket_name, 
                    object_key, 
                    part_number, 
                    upload_id, 
                    data
                )
                
                if resp.status >= 300:
                    print(f"上传分片 {part_number} 失败: {resp.errorMessage}")
                    # 取消分片上传任务
                    obs_client.abortMultipartUpload(bucket_name, object_key, upload_id)
                    return False
                    
                parts.append({
                    'PartNumber': part_number,
                    'ETag': resp.etag
                })
                part_number += 1
                
                # 显示进度
                uploaded = min((part_number-1)*part_size, file_size)
                progress = (uploaded / file_size) * 100
                print(f"上传进度: {progress:.1f}% ({uploaded}/{file_size} 字节)")
        
        # 合并分片
        resp = obs_client.completeMultipartUpload(
            bucket_name, 
            object_key, 
            upload_id, 
            parts
        )
        
        if resp.status < 300:
            print(f"大文件上传成功: {object_key}")
            return True
        else:
            print(f"合并分片失败: {resp.errorMessage}")
            return False
            
    except Exception as e:
        print(f"上传大文件异常: {e}")
        if 'upload_id' in locals():
            obs_client.abortMultipartUpload(bucket_name, object_key, upload_id)
        return False
```

## 下载文件
```python
def download_file(obs_client, bucket_name, object_key, local_file_path):
    """
    从 OBS 下载文件
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_key: OBS 中的对象路径
        local_file_path: 本地保存路径
        
    Returns:
        bool: 下载是否成功
    """
    try:
        resp = obs_client.getObject(bucket_name, object_key, downloadPath=local_file_path)
        if resp.status < 300:
            print(f"文件下载成功: {local_file_path}")
            return True
        else:
            print(f"文件下载失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"下载文件异常: {e}")
        return False
```

## 删除对象
```python
def delete_object(obs_client, bucket_name, object_key):
    """
    删除单个对象
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_key: OBS 中的对象路径
        
    Returns:
        bool: 删除是否成功
    """
    try:
        resp = obs_client.deleteObject(bucket_name, object_key)
        if resp.status < 300:
            print(f"对象删除成功: {object_key}")
            return True
        else:
            print(f"对象删除失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"删除对象异常: {e}")
        return False
```

## 批量删除对象
```python
def delete_objects(obs_client, bucket_name, object_keys):
    """
    批量删除对象
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_keys: 对象路径列表
        
    Returns:
        dict: 删除结果，包含成功和失败的对象列表
    """
    try:
        objects = [{'key': key} for key in object_keys]
        resp = obs_client.deleteObjects(bucket_name, objects=objects, quiet=False)
        
        if resp.status < 300:
            deleted = [obj.key for obj in resp.body.deleted]
            errors = [{'key': err.key, 'message': err.message} for err in resp.body.error]
            
            print(f"批量删除完成: 成功 {len(deleted)} 个，失败 {len(errors)} 个")
            return {
                'success': True,
                'deleted': deleted,
                'errors': errors
            }
        else:
            print(f"批量删除失败: {resp.errorMessage}")
            return {
                'success': False,
                'error': resp.errorMessage
            }
    except Exception as e:
        print(f"批量删除异常: {e}")
        return {
            'success': False,
            'error': str(e)
        }
```

## 列举对象
```python
def list_objects(obs_client, bucket_name, prefix='', delimiter='', max_keys=1000):
    """
    列举存储桶中的对象
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        prefix: 对象前缀，用于过滤
        delimiter: 分隔符，用于按目录结构列举
        max_keys: 最大返回数量
        
    Returns:
        list: 对象列表，每个元素包含 key, size, last_modified 等信息
    """
    try:
        objects = []
        marker = None
        
        while True:
            resp = obs_client.listObjects(
                bucket_name,
                prefix=prefix,
                delimiter=delimiter,
                marker=marker,
                max_keys=max_keys
            )
            
            if resp.status >= 300:
                print(f"列举对象失败: {resp.errorMessage}")
                return []
                
            for content in resp.body.contents:
                objects.append({
                    'key': content.key,
                    'size': content.size,
                    'last_modified': content.lastModified,
                    'etag': content.etag
                })
                
            # 检查是否还有更多对象
            if not resp.body.is_truncated:
                break
            marker = resp.body.next_marker
        
        print(f"共找到 {len(objects)} 个对象")
        return objects
    except Exception as e:
        print(f"列举对象异常: {e}")
        return []
```

## 生成预签名 URL
```python
def generate_presigned_url(obs_client, bucket_name, object_key, expires=3600):
    """
    生成对象的预签名访问 URL（临时授权访问）
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        object_key: OBS 中的对象路径
        expires: 过期时间，单位秒，默认 3600 秒（1小时）
        
    Returns:
        str: 预签名 URL，失败返回 None
    """
    try:
        resp = obs_client.createSignedUrl(
            'GET',
            bucket_name,
            object_key,
            expires=expires
        )
        
        if resp.status < 300:
            return resp.signedUrl
        else:
            print(f"生成预签名 URL 失败: {resp.errorMessage}")
            return None
    except Exception as e:
        print(f"生成预签名 URL 异常: {e}")
        return None
```
