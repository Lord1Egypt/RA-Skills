#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为云 OBS 通用工具脚本
提供常用的 OBS 操作封装
"""

import os
from obs import ObsClient
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_obs_client(ak=None, sk=None, server=None):
    """
    获取 OBS 客户端实例
    
    Args:
        ak: 访问密钥 AK，如果为 None 则从环境变量 OBS_AK 读取
        sk: 访问密钥 SK，如果为 None 则从环境变量 OBS_SK 读取
        server: OBS 服务端点，如果为 None 则从环境变量 OBS_SERVER 读取，默认 obs.cn-east-3.myhuaweicloud.com
        
    Returns:
        ObsClient 实例或 None
    """
    ak = ak or os.getenv('OBS_AK')
    sk = sk or os.getenv('OBS_SK')
    server = server or os.getenv('OBS_SERVER', 'obs.cn-east-3.myhuaweicloud.com')
    
    if not ak or not sk:
        print("错误：缺少 OBS_AK 或 OBS_SK 环境变量")
        return None
        
    try:
        client = ObsClient(
            access_key_id=ak,
            secret_access_key=sk,
            server=server
        )
        print("OBS 客户端初始化成功")
        return client
    except Exception as e:
        print(f"OBS 客户端初始化失败: {e}")
        return None

def upload_file(obs_client, bucket_name, object_key, local_file_path):
    """上传单个文件"""
    try:
        resp = obs_client.putFile(bucket_name, object_key, local_file_path)
        return resp.status < 300, resp.errorMessage if resp.status >= 300 else None
    except Exception as e:
        return False, str(e)

def download_file(obs_client, bucket_name, object_key, local_file_path):
    """下载单个文件"""
    try:
        resp = obs_client.getObject(bucket_name, object_key, downloadPath=local_file_path)
        return resp.status < 300, resp.errorMessage if resp.status >= 300 else None
    except Exception as e:
        return False, str(e)

def list_objects(obs_client, bucket_name, prefix='', max_keys=1000):
    """列举对象"""
    try:
        objects = []
        marker = None
        
        while True:
            resp = obs_client.listObjects(
                bucket_name,
                prefix=prefix,
                marker=marker,
                max_keys=max_keys
            )
            
            if resp.status >= 300:
                return None, resp.errorMessage
                
            for content in resp.body.contents:
                objects.append({
                    'key': content.key,
                    'size': content.size,
                    'last_modified': content.lastModified,
                    'etag': content.etag
                })
                
            if not resp.body.is_truncated:
                break
            marker = resp.body.next_marker
        
        return objects, None
    except Exception as e:
        return None, str(e)

def delete_object(obs_client, bucket_name, object_key):
    """删除单个对象"""
    try:
        resp = obs_client.deleteObject(bucket_name, object_key)
        return resp.status < 300, resp.errorMessage if resp.status >= 300 else None
    except Exception as e:
        return False, str(e)

def generate_presigned_url(obs_client, bucket_name, object_key, expires=3600):
    """生成预签名 URL"""
    try:
        resp = obs_client.createSignedUrl(
            'GET',
            bucket_name,
            object_key,
            expires=expires
        )
        if resp.status < 300:
            return resp.signedUrl, None
        else:
            return None, resp.errorMessage
    except Exception as e:
        return None, str(e)

if __name__ == '__main__':
    # 示例用法
    client = get_obs_client()
    if not client:
        exit(1)
        
    # 示例：列举所有存储桶
    try:
        resp = client.listBuckets()
        if resp.status < 300:
            print("存储桶列表:")
            for bucket in resp.body.buckets:
                print(f"  - {bucket.name} (创建时间: {bucket.creationDate})")
    except Exception as e:
        print(f"列举存储桶失败: {e}")
        
    client.close()
