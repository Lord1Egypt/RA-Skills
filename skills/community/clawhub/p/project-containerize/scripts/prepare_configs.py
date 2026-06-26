#!/usr/bin/env python3
"""
配置文件准备脚本 - 阶段4
根据阶段1分析结果，准备配置文件模板
"""

import os
import shutil
from pathlib import Path


def find_config_files(project_path):
    """查找项目中的配置文件"""
    configs = []

    # 常见的配置文件模式
    config_patterns = [
        'application*.yml', 'application*.yaml', 'application*.properties',
        'config*.yml', 'config*.yaml', 'config*.json', 'config*.ini',
        '*.config.js', '*.config.ts',
        'nginx.conf', 'httpd.conf',
        'logback.xml', 'log4j*.xml',
        '.env*', 'config.env'
    ]

    import glob
    for pattern in config_patterns:
        matches = glob.glob(os.path.join(project_path, '**', pattern), recursive=True)
        for match in matches:
            # 排除 node_modules 等目录
            if any(excluded in match for excluded in ['node_modules', '.git', 'target', 'build', 'dist']):
                continue
            configs.append(match)

    return configs


def copy_configs_to_deploy(project_path):
    """将配置文件复制到 deploy/config/ 目录"""
    deploy_config_dir = os.path.join(project_path, 'deploy', 'config')
    os.makedirs(deploy_config_dir, exist_ok=True)

    configs = find_config_files(project_path)
    copied = []

    for config_path in configs:
        # 计算相对路径
        rel_path = os.path.relpath(config_path, project_path)

        # 目标路径
        dest_path = os.path.join(deploy_config_dir, rel_path)
        dest_dir = os.path.dirname(dest_path)

        # 创建目标目录
        os.makedirs(dest_dir, exist_ok=True)

        # 复制文件
        shutil.copy2(config_path, dest_path)
        copied.append(rel_path)

    return copied


def generate_env_template(project_path):
    """生成环境变量模板"""
    env_content = """# 应用基础配置
APP_NAME=myapp
APP_PORT=8080
APP_ENV=production
LOG_LEVEL=info

# 数据库配置（根据项目调整）
# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=mydb
# DB_USER=root
# DB_PASSWORD=changeme

# 缓存配置（根据项目调整）
# REDIS_HOST=localhost
# REDIS_PORT=6379
# REDIS_PASSWORD=

# 消息队列配置（根据项目调整）
# RABBITMQ_HOST=localhost
# RABBITMQ_PORT=5672
# RABBITMQ_USER=guest
# RABBITMQ_PASSWORD=guest

# 其他服务配置（根据项目调整）
# API_BASE_URL=http://localhost:8080
# JWT_SECRET=your-secret-key
"""

    env_path = os.path.join(project_path, 'deploy', '.env')
    with open(env_path, 'w') as f:
        f.write(env_content)

    return env_path


def generate_config_readme(project_path, copied_configs):
    """生成配置说明文档"""
    readme_content = """# 配置说明

本文档说明如何配置项目运行所需的各项参数。

## 配置文件清单

"""

    if copied_configs:
        readme_content += "### 从项目复制的配置文件\n\n"
        for cfg in copied_configs:
            readme_content += f"- `{cfg}`\n"
        readme_content += "\n"

    readme_content += """### 环境变量文件

- `.env` - 环境变量配置文件

## 配置挂载说明

在部署时，配置文件将挂载到容器内的指定路径：

| 本地路径 | 容器内路径 | 说明 |
|---------|-----------|------|
"""

    # 根据复制的配置文件生成挂载说明
    for cfg in copied_configs:
        if 'application' in cfg:
            container_path = "/app/config/application.yml"
        elif 'nginx' in cfg:
            container_path = "/etc/nginx/conf.d/default.conf"
        elif 'logback' in cfg or 'log4j' in cfg:
            container_path = f"/app/{cfg}"
        else:
            container_path = f"/app/config/{os.path.basename(cfg)}"

        readme_content += f"| `config/{cfg}` | `{container_path}` | 应用配置 |\n"

    readme_content += """
## 如何修改配置

1. **环境变量**：编辑 `.env` 文件，修改对应的环境变量值
2. **应用配置**：编辑 `config/` 目录下的配置文件
3. **重启生效**：修改配置后需要重启容器才能生效

## 配置热加载

部分配置支持热加载（无需重启），具体取决于应用框架的支持：

- **日志级别**：通常支持热加载
- **部分业务配置**：取决于具体实现
- **数据库连接等核心配置**：通常需要重启

## 安全注意事项

1. 不要将包含敏感信息的配置文件提交到版本控制
2. 生产环境使用强密码
3. 定期轮换密钥和凭证
4. 使用只读挂载（`:ro`）防止容器内修改配置
"""

    config_md_path = os.path.join(project_path, 'deploy', 'CONFIG.md')
    with open(config_md_path, 'w') as f:
        f.write(readme_content)

    return config_md_path


def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: python prepare_configs.py <项目路径>")
        sys.exit(1)

    project_path = sys.argv[1]

    # 复制配置文件
    copied = copy_configs_to_deploy(project_path)
    if copied:
        print(f"已复制 {len(copied)} 个配置文件到 deploy/config/")
        for cfg in copied:
            print(f"  - {cfg}")
    else:
        print("未找到配置文件")

    # 生成环境变量模板
    env_path = generate_env_template(project_path)
    print(f"\n环境变量模板已生成: {env_path}")

    # 生成配置说明文档
    config_md_path = generate_config_readme(project_path, copied)
    print(f"配置说明文档已生成: {config_md_path}")


if __name__ == '__main__':
    main()
