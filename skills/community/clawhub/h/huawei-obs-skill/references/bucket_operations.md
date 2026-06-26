# 存储桶操作指南

## 创建存储桶
```python
from obs import CreateBucketHeader

def create_bucket(obs_client, bucket_name, location='cn-east-3'):
    """
    创建存储桶
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称（全局唯一，3-63字符）
        location: 区域，默认 cn-east-3
        
    Returns:
        bool: 创建是否成功
    """
    try:
        headers = CreateBucketHeader()
        headers.location = location
        resp = obs_client.createBucket(bucket_name, headers=headers)
        
        if resp.status < 300:
            print(f"存储桶 {bucket_name} 创建成功")
            return True
        else:
            print(f"存储桶创建失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"创建存储桶异常: {e}")
        return False
```

## 删除存储桶
```python
def delete_bucket(obs_client, bucket_name):
    """
    删除存储桶（注意：存储桶必须为空才能删除）
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        
    Returns:
        bool: 删除是否成功
    """
    try:
        resp = obs_client.deleteBucket(bucket_name)
        if resp.status < 300:
            print(f"存储桶 {bucket_name} 删除成功")
            return True
        else:
            print(f"存储桶删除失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"删除存储桶异常: {e}")
        return False
```

## 判断存储桶是否存在
```python
def bucket_exists(obs_client, bucket_name):
    """
    判断存储桶是否存在
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        
    Returns:
        bool: 存储桶是否存在
    """
    try:
        resp = obs_client.headBucket(bucket_name)
        return resp.status < 300
    except Exception as e:
        print(f"检查存储桶存在性异常: {e}")
        return False
```

## 列举所有存储桶
```python
def list_buckets(obs_client):
    """
    列举所有存储桶
    
    Args:
        obs_client: OBS 客户端实例
        
    Returns:
        list: 存储桶列表，每个元素是存储桶信息字典
    """
    try:
        resp = obs_client.listBuckets()
        if resp.status < 300:
            buckets = []
            for bucket in resp.body.buckets:
                buckets.append({
                    'name': bucket.name,
                    'creation_date': bucket.creationDate,
                    'location': bucket.location
                })
            return buckets
        else:
            print(f"列举存储桶失败: {resp.errorMessage}")
            return []
    except Exception as e:
        print(f"列举存储桶异常: {e}")
        return []
```

## 设置存储桶权限
```python
from obs import AccessControlList, Grant, Permission, Group

def set_bucket_public_read(obs_client, bucket_name):
    """
    设置存储桶为公开读权限
    
    Args:
        obs_client: OBS 客户端实例
        bucket_name: 存储桶名称
        
    Returns:
        bool: 设置是否成功
    """
    try:
        acl = AccessControlList()
        grant = Grant()
        grant.grantee = Group.ALL_USERS
        grant.permission = Permission.PERMISSION_READ
        acl.grants.append(grant)
        
        resp = obs_client.setBucketAcl(bucket_name, acl)
        if resp.status < 300:
            print(f"存储桶 {bucket_name} 已设置为公开读权限")
            return True
        else:
            print(f"设置存储桶权限失败: {resp.errorMessage}")
            return False
    except Exception as e:
        print(f"设置存储桶权限异常: {e}")
        return False
```
