#!/usr/bin/env python3
"""
产品设计工作流 - 上传Demo到服务器通用脚本
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='上传Demo到服务器')
    parser.add_argument('--date', type=str, required=True, help='日期（YYYY-MM-DD）')
    parser.add_argument('--slugs', type=str, nargs='+', required=True, help='Demo目录的slug列表（空格分隔）')
    parser.add_argument('--local-ideas-dir', type=str, default='./ideas', help='本地ideas目录')
    parser.add_argument('--server-host', type=str, required=True, help='服务器主机地址（例如：192.168.8.50）')
    parser.add_argument('--server-user', type=str, required=True, help='服务器用户名（例如：dixai）')
    parser.add_argument('--server-pass', type=str, required=True, help='服务器密码')
    parser.add_argument('--server-path', type=str, required=True, help='服务器路径（例如：/www/wwwroot/demo/）')
    parser.add_argument('--preview-domain', type=str, required=True, help='预览域名（例如：http://demo.yourdomain.com）')
    return parser.parse_args()

def run_cmd(cmd):
    """执行命令"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"异常: {e}")
        return False

def upload_demo(date_str, slug, local_ideas_dir, server_host, server_user, server_pass, server_path):
    """上传单个Demo"""
    local_dir = os.path.join(local_ideas_dir, f'{date_str}-{slug}', 'demo')
    remote_dir = os.path.join(server_path, f'{date_str}-{slug}', 'demo')
    
    if not os.path.exists(local_dir):
        print(f"本地目录不存在: {local_dir}")
        return False
    
    # 创建远程目录
    print(f"创建远程目录: {remote_dir}")
    mkdir_cmd = f"sshpass -p '{server_pass}' ssh -o StrictHostKeyChecking=no {server_user}@{server_host} 'mkdir -p {remote_dir}'"
    if not run_cmd(mkdir_cmd):
        return False
    
    # 上传文件
    print(f"上传文件: {local_dir} -> {remote_dir}")
    scp_cmd = f"sshpass -p '{server_pass}' scp -o StrictHostKeyChecking=no -r {local_dir}/* {server_user}@{server_host}:{remote_dir}/"
    return run_cmd(scp_cmd)

def main():
    """主函数"""
    args = parse_args()
    
    print("=" * 60)
    print("产品设计工作流 - 上传Demo到服务器")
    print("=" * 60)
    
    success_count = 0
    for slug in args.slugs:
        print(f"\n上传: {slug}")
        if upload_demo(
            args.date, slug, args.local_ideas_dir,
            args.server_host, args.server_user, args.server_pass, args.server_path
        ):
            success_count += 1
            print(f"✅ {slug} 上传成功")
        else:
            print(f"❌ {slug} 上传失败")
    
    print(f"\n上传完成: {success_count}/{len(args.slugs)} 成功")
    
    # 打印预览地址
    print(f"\n预览地址:")
    for slug in args.slugs:
        print(f"  {args.preview_domain}/{args.date}-{slug}/demo/")

if __name__ == '__main__':
    main()
