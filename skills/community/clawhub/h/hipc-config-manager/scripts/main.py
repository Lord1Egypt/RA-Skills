import argparse
import json
import os
import sys
import re  # 引入正则模块

# 获取当前脚本所在的目录
BASE_DIR = os.path.expanduser("~")
# 拼接出配置文件的绝对路径
CONFIG_FILE = os.path.join(BASE_DIR, "hipc_config.json")


def read_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def write_config(data):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def is_valid_secret(secret):
    """
    校验规则：必须以 '数字_' 开头，后面跟至少 5 个字符
    例如：35097_y2GX52eDGNdgaM
    """
    if not secret:
        return False
    # 正则：^\d+_ 表示以数字和下划线开头， .{5,} 表示后面至少跟 5 个字符
    pattern = r"^\d+_.{5,}"
    return re.match(pattern, secret) is not None


def check_action():
    config = read_config()
    secret = config.get('hipc_secret', '')

    if secret and len(secret) > 0:
        result = {"status": "success", "message": "环境检查通过，密钥已配置。","is_configured": True}
    else:
        result = {"status": "error", "message": "未检测到 HIPC 密钥。", "is_configured": False}

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result['is_configured']: sys.exit(1)


def set_action(secret,env):
    # 1. 先进行格式校验
    if not is_valid_secret(secret):
        # 如果格式不对，直接返回错误 JSON，不写入文件
        error_result = {
            "status": "error",
            "message": "密钥格式无效！请检查密钥格式是否正确。",
            "is_configured": False
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
        sys.exit(1)  # 退出码 1 表示失败

    # 2. 格式正确，才执行保存
    config = read_config()
    config['hipc_secret'] = secret
    if env == 'prod':
        config['host'] = "api.hipcapi.com"
    else:
        config['host'] = "api-beta.hipcapi.com"

    write_config(config)

    print(json.dumps({
        "status": "success",
        "message": "HIPC 密钥已成功保存！",
        "is_configured": True
    }, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', type=str, required=True, choices=['check', 'set'])
    parser.add_argument('--secret', type=str, required=False)
    parser.add_argument('--env', type=str, required=False,default='prod', choices=['dev', 'prod'])

    args = parser.parse_args()

    if args.action == 'check':
        check_action()
    elif args.action == 'set':
        if not args.secret:
            print(json.dumps({"status": "error", "message": "缺少 secret 参数"}))
            sys.exit(1)
        set_action(args.secret,args.env)