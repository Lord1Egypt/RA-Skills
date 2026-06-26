# Ansible 自动化编排参考文档

> 覆盖 Ansible 核心概念、Inventory、Playbook、Role、Vault、Galaxy、AWX/Tower、最佳实践与故障排查。

---

## 目录

- [1. Ansible 基础](#1-ansible-基础)
- [2. Inventory 管理](#2-inventory-管理)
- [3. Playbook 编写](#3-playbook-编写)
- [4. Role 组织](#4-role-组织)
- [5. 变量与模板](#5-变量与模板)
- [6. Vault 加密](#6-vault-加密)
- [7. Galaxy 与集合](#7-galaxy-与集合)
- [8. AWX/Tower](#8-awxtower)
- [9. 性能优化](#9-性能优化)
- [10. 最佳实践](#10-最佳实践)
- [11. 故障排查](#11-故障排查)

---

## 1. Ansible 基础

### 1.1 安装

```bash
# pip 安装（推荐）
pip3 install ansible ansible-lint

# 系统包安装
# RHEL/CentOS
dnf install ansible-core

# Ubuntu/Debian
apt install ansible

# 验证安装
ansible --version
ansible-config dump --only-changed
```

### 1.2 核心概念

```text
控制节点 (Control Node)
  ├── Inventory — 管理的主机清单
  ├── Playbook — 自动化任务剧本（YAML）
  ├── Module — 执行具体操作的模块（如 apt、yum、copy、service）
  ├── Role — 可复用的任务集合（标准目录结构）
  ├── Plugin — 扩展功能（connection、callback、filter 等）
  └── Vault — 加密敏感数据

被管理节点 (Managed Node)
  ├── 需要 SSH 访问（Linux）或 WinRM（Windows）
  ├── 需要 Python（Linux）或 PowerShell（Windows）
  └── 无需安装 Agent（Agentless 架构）
```

### 1.3 配置文件

```ini
# ansible.cfg（优先级：ANSIBLE_CONFIG > ./ansible.cfg > ~/.ansible.cfg > /etc/ansible/ansible.cfg）
[defaults]
inventory = ./inventory/
roles_path = ./roles/
collections_paths = ./collections/
remote_user = deploy
private_key_file = ~/.ssh/id_ed25519
host_key_checking = False
retry_files_enabled = False
stdout_callback = yaml
callbacks_enabled = timer, profile_tasks
forks = 20
timeout = 30
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 3600

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False

[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o PreferredAuthentications=publickey
control_path_dir = /tmp/.ansible-cp
```

### 1.4 Ad-hoc 命令

```bash
# 测试连通性
ansible all -m ping

# 执行命令
ansible webservers -m shell -a "uptime"

# 复制文件
ansible all -m copy -a "src=/etc/hosts dest=/tmp/hosts"

# 安装软件包
ansible webservers -m apt -a "name=nginx state=present" --become

# 管理服务
ansible webservers -m service -a "name=nginx state=started enabled=yes" --become

# 查看 facts
ansible hostname -m setup -a "filter=ansible_distribution*"

# 限定主机
ansible all -m ping --limit "web01,web02"

# 并行度控制
ansible all -m ping -f 50
```

---

## 2. Inventory 管理

### 2.1 静态 Inventory（INI 格式）

```ini
# inventory/hosts.ini
[webservers]
web01 ansible_host=192.168.1.10 ansible_port=22
web02 ansible_host=192.168.1.11
web03 ansible_host=192.168.1.12

[dbservers]
db01 ansible_host=192.168.1.20
db02 ansible_host=192.168.1.21

[loadbalancers]
lb01 ansible_host=192.168.1.5

# 子组
[production:children]
webservers
dbservers
loadbalancers

# 组变量
[webservers:vars]
http_port=80
ansible_user=deploy

[dbservers:vars]
db_port=3306

# 范围表达式
[app_servers]
app[01:20].example.com
```

### 2.2 静态 Inventory（YAML 格式）

```yaml
# inventory/hosts.yaml
all:
  children:
    production:
      children:
        webservers:
          hosts:
            web01:
              ansible_host: 192.168.1.10
              http_port: 80
            web02:
              ansible_host: 192.168.1.11
            web03:
              ansible_host: 192.168.1.12
          vars:
            ansible_user: deploy
        dbservers:
          hosts:
            db01:
              ansible_host: 192.168.1.20
            db02:
              ansible_host: 192.168.1.21
          vars:
            db_port: 3306
    staging:
      hosts:
        staging01:
          ansible_host: 10.0.1.10
```

### 2.3 动态 Inventory

```bash
# AWS EC2 动态 Inventory（使用 aws_ec2 插件）
# inventory/aws_ec2.yaml
plugin: amazon.aws.aws_ec2
regions:
  - ap-southeast-1
  - us-east-1
filters:
  tag:Environment:
    - production
    - staging
  instance-state-name: running
keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.region
    prefix: region
hostnames:
  - private-ip-address
compose:
  ansible_host: private_ip_address
```

```python
#!/usr/bin/env python3
# inventory/custom_inventory.py — 自定义动态 Inventory 脚本
import json
import sys

def get_inventory():
    return {
        "webservers": {
            "hosts": ["web01", "web02"],
            "vars": {"http_port": 80}
        },
        "_meta": {
            "hostvars": {
                "web01": {"ansible_host": "192.168.1.10"},
                "web02": {"ansible_host": "192.168.1.11"}
            }
        }
    }

if __name__ == "__main__":
    if "--list" in sys.argv:
        print(json.dumps(get_inventory(), indent=2))
    elif "--host" in sys.argv:
        print(json.dumps({}))
```

### 2.4 Inventory 变量目录结构

```text
inventory/
├── hosts.yaml              # 主机清单
├── group_vars/
│   ├── all.yaml            # 所有主机的变量
│   ├── webservers.yaml     # webservers 组变量
│   ├── dbservers.yaml      # dbservers 组变量
│   └── production/
│       ├── vars.yaml       # production 组变量
│       └── vault.yaml      # production 加密变量
└── host_vars/
    ├── web01.yaml           # web01 主机变量
    └── db01.yaml            # db01 主机变量
```

---

## 3. Playbook 编写

### 3.1 基本结构

```yaml
---
# playbooks/deploy_web.yaml
- name: 部署 Web 服务器
  hosts: webservers
  become: yes
  gather_facts: yes
  vars:
    app_version: "2.1.0"
    app_port: 8080

  pre_tasks:
    - name: 更新 apt 缓存
      apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"

  tasks:
    - name: 安装必要软件包
      package:
        name:
          - nginx
          - python3
          - python3-pip
        state: present

    - name: 部署 Nginx 配置
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/sites-available/myapp
        owner: root
        group: root
        mode: '0644'
      notify: reload nginx

    - name: 启用站点
      file:
        src: /etc/nginx/sites-available/myapp
        dest: /etc/nginx/sites-enabled/myapp
        state: link
      notify: reload nginx

    - name: 确保 Nginx 运行
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded

  post_tasks:
    - name: 健康检查
      uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      retries: 5
      delay: 3
```

### 3.2 常用模块

```yaml
# 文件操作
- name: 复制文件
  copy:
    src: files/app.conf
    dest: /etc/app/app.conf
    owner: app
    group: app
    mode: '0640'
    backup: yes

- name: 使用模板
  template:
    src: templates/config.j2
    dest: /etc/app/config.yaml
    validate: "python3 -c 'import yaml; yaml.safe_load(open(\"%s\"))'"

- name: 创建目录
  file:
    path: /opt/app/data
    state: directory
    owner: app
    group: app
    mode: '0755'
    recurse: yes

- name: 下载文件
  get_url:
    url: "https://example.com/app-{{ version }}.tar.gz"
    dest: /tmp/app.tar.gz
    checksum: "sha256:abc123..."

- name: 解压文件
  unarchive:
    src: /tmp/app.tar.gz
    dest: /opt/app/
    remote_src: yes
    creates: /opt/app/bin/server

# 用户管理
- name: 创建应用用户
  user:
    name: app
    system: yes
    shell: /usr/sbin/nologin
    home: /opt/app
    create_home: yes

# 系统管理
- name: 设置内核参数
  sysctl:
    name: net.core.somaxconn
    value: '65535'
    state: present
    reload: yes

- name: 管理 cron 任务
  cron:
    name: "清理日志"
    minute: "0"
    hour: "3"
    job: "find /var/log/app -name '*.log' -mtime +30 -delete"
    user: root

# 条件判断
- name: 仅在 CentOS 上执行
  yum:
    name: epel-release
    state: present
  when: ansible_distribution == "CentOS"

# 循环
- name: 创建多个用户
  user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
    state: present
  loop:
    - { name: 'alice', groups: 'sudo,docker' }
    - { name: 'bob', groups: 'docker' }

# 注册变量
- name: 检查服务状态
  command: systemctl is-active nginx
  register: nginx_status
  ignore_errors: yes

- name: 启动 Nginx（如果未运行）
  service:
    name: nginx
    state: started
  when: nginx_status.rc != 0

# 错误处理
- name: 尝试操作（允许失败）
  block:
    - name: 执行主操作
      command: /opt/app/bin/migrate
  rescue:
    - name: 回滚
      command: /opt/app/bin/rollback
  always:
    - name: 清理临时文件
      file:
        path: /tmp/migration_lock
        state: absent
```

### 3.3 Playbook 执行

```bash
# 基本执行
ansible-playbook playbooks/deploy_web.yaml

# 指定 inventory
ansible-playbook -i inventory/production playbooks/deploy.yaml

# 限定主机
ansible-playbook playbooks/deploy.yaml --limit "web01,web02"

# 传递变量
ansible-playbook playbooks/deploy.yaml -e "app_version=2.2.0"

# Dry-run（检查模式）
ansible-playbook playbooks/deploy.yaml --check --diff

# 逐步执行
ansible-playbook playbooks/deploy.yaml --step

# 从指定任务开始
ansible-playbook playbooks/deploy.yaml --start-at-task="部署 Nginx 配置"

# 标签过滤
ansible-playbook playbooks/deploy.yaml --tags "config,deploy"
ansible-playbook playbooks/deploy.yaml --skip-tags "test"

# 详细输出
ansible-playbook playbooks/deploy.yaml -vvv

# Vault 密码
ansible-playbook playbooks/deploy.yaml --ask-vault-pass
ansible-playbook playbooks/deploy.yaml --vault-password-file=~/.vault_pass
```

---

## 4. Role 组织

### 4.1 Role 目录结构

```text
roles/
└── nginx/
    ├── defaults/
    │   └── main.yaml       # 默认变量（最低优先级）
    ├── vars/
    │   └── main.yaml       # 角色变量（高优先级）
    ├── tasks/
    │   ├── main.yaml       # 任务入口
    │   ├── install.yaml    # 安装任务
    │   ├── config.yaml     # 配置任务
    │   └── service.yaml    # 服务管理
    ├── handlers/
    │   └── main.yaml       # 处理程序
    ├── templates/
    │   ├── nginx.conf.j2
    │   └── vhost.conf.j2
    ├── files/
    │   └── ssl/
    ├── meta/
    │   └── main.yaml       # 角色元数据（依赖）
    ├── tests/
    │   ├── inventory
    │   └── test.yaml
    └── README.md
```

### 4.2 Role 示例

```yaml
# roles/nginx/defaults/main.yaml
---
nginx_worker_processes: auto
nginx_worker_connections: 1024
nginx_keepalive_timeout: 65
nginx_client_max_body_size: "10m"
nginx_vhosts: []
nginx_ssl_protocols: "TLSv1.2 TLSv1.3"
nginx_ssl_ciphers: "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256"

# roles/nginx/tasks/main.yaml
---
- name: 加载 OS 特定变量
  include_vars: "{{ ansible_os_family }}.yaml"

- import_tasks: install.yaml
  tags: [nginx, install]

- import_tasks: config.yaml
  tags: [nginx, config]

- import_tasks: service.yaml
  tags: [nginx, service]

# roles/nginx/tasks/install.yaml
---
- name: 安装 Nginx
  package:
    name: nginx
    state: present

- name: 创建配置目录
  file:
    path: "{{ item }}"
    state: directory
    owner: root
    group: root
    mode: '0755'
  loop:
    - /etc/nginx/conf.d
    - /etc/nginx/sites-available
    - /etc/nginx/sites-enabled
    - /etc/nginx/ssl

# roles/nginx/handlers/main.yaml
---
- name: reload nginx
  service:
    name: nginx
    state: reloaded
  listen: "reload nginx"

- name: restart nginx
  service:
    name: nginx
    state: restarted
  listen: "restart nginx"

# roles/nginx/meta/main.yaml
---
galaxy_info:
  role_name: nginx
  author: sysadmin
  description: Nginx web server role
  min_ansible_version: "2.14"
  platforms:
    - name: Ubuntu
      versions: [focal, jammy]
    - name: EL
      versions: [8, 9]

dependencies:
  - role: common
    vars:
      common_packages:
        - curl
        - openssl
```

### 4.3 在 Playbook 中使用 Role

```yaml
---
- name: 部署 Web 集群
  hosts: webservers
  become: yes

  roles:
    - role: common
    - role: nginx
      vars:
        nginx_worker_connections: 4096
        nginx_vhosts:
          - server_name: www.example.com
            root: /var/www/html
            ssl: true
    - role: app_deploy
      tags: [deploy]
```

---

## 5. 变量与模板

### 5.1 变量优先级（从低到高）

```text
1.  command line values (e.g. -u user)
2.  role defaults (roles/x/defaults/main.yaml)
3.  inventory file or script group vars
4.  inventory group_vars/all
5.  playbook group_vars/all
6.  inventory group_vars/*
7.  playbook group_vars/*
8.  inventory file or script host vars
9.  inventory host_vars/*
10. playbook host_vars/*
11. host facts / cached set_facts
12. play vars
13. play vars_prompt
14. play vars_files
15. role vars (roles/x/vars/main.yaml)
16. block vars (only for tasks in block)
17. task vars (only for the task)
18. include_vars
19. set_facts / registered vars
20. role (and include_role) params
21. include params
22. extra vars (-e "key=value")  ← 最高优先级
```

### 5.2 Jinja2 模板

```jinja2
{# templates/nginx.conf.j2 #}
# Ansible managed — DO NOT EDIT MANUALLY
# Generated on {{ ansible_date_time.iso8601 }}

user www-data;
worker_processes {{ nginx_worker_processes }};
pid /run/nginx.pid;

events {
    worker_connections {{ nginx_worker_connections }};
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    keepalive_timeout {{ nginx_keepalive_timeout }};
    client_max_body_size {{ nginx_client_max_body_size }};

    # SSL 配置
    ssl_protocols {{ nginx_ssl_protocols }};
    ssl_ciphers '{{ nginx_ssl_ciphers }}';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

{% for vhost in nginx_vhosts %}
    server {
        listen {{ '443 ssl' if vhost.ssl | default(false) else '80' }};
        server_name {{ vhost.server_name }};
        root {{ vhost.root | default('/var/www/html') }};

{% if vhost.ssl | default(false) %}
        ssl_certificate /etc/nginx/ssl/{{ vhost.server_name }}.crt;
        ssl_certificate_key /etc/nginx/ssl/{{ vhost.server_name }}.key;
{% endif %}

{% if vhost.locations is defined %}
{% for location in vhost.locations %}
        location {{ location.path }} {
            proxy_pass {{ location.proxy_pass }};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
{% endfor %}
{% endif %}
    }
{% endfor %}
}
```

### 5.3 常用 Jinja2 过滤器

```yaml
# 字符串操作
"{{ hostname | upper }}"              # 大写
"{{ path | basename }}"               # 文件名
"{{ path | dirname }}"                # 目录名
"{{ list | join(',') }}"              # 列表拼接
"{{ password | password_hash('sha512') }}"  # 密码哈希

# 默认值
"{{ variable | default('fallback') }}"
"{{ variable | default(omit) }}"      # 未定义时省略参数

# 列表操作
"{{ users | map(attribute='name') | list }}"
"{{ packages | unique | sort }}"
"{{ list1 | union(list2) }}"
"{{ list1 | intersect(list2) }}"

# 数据格式
"{{ data | to_json }}"
"{{ data | to_yaml }}"
"{{ data | to_nice_json(indent=2) }}"

# 正则
"{{ string | regex_search('pattern') }}"
"{{ string | regex_replace('old', 'new') }}"

# IP 地址
"{{ '192.168.1.0/24' | ipaddr('network') }}"
"{{ ansible_default_ipv4.address | ipaddr }}"

# 文件
"{{ lookup('file', '/etc/hostname') }}"
"{{ lookup('env', 'HOME') }}"
"{{ lookup('password', '/tmp/pass length=16 chars=ascii_letters,digits') }}"
```

---

## 6. Vault 加密

### 6.1 基本操作

```bash
# 创建加密文件
ansible-vault create secrets.yaml

# 编辑加密文件
ansible-vault edit secrets.yaml

# 加密已有文件
ansible-vault encrypt vars/production.yaml

# 解密文件
ansible-vault decrypt vars/production.yaml

# 查看加密文件
ansible-vault view secrets.yaml

# 更换密码
ansible-vault rekey secrets.yaml

# 加密单个字符串（内联加密）
ansible-vault encrypt_string 'SuperSecretPassword' --name 'db_password'
# 输出：
# db_password: !vault |
#   $ANSIBLE_VAULT;1.1;AES256
#   ...加密内容...
```

### 6.2 多 Vault ID

```bash
# 使用不同的 Vault ID 管理不同环境的密钥
ansible-vault create --vault-id prod@prompt secrets_prod.yaml
ansible-vault create --vault-id dev@prompt secrets_dev.yaml

# 执行时指定多个 Vault ID
ansible-playbook site.yaml \
  --vault-id dev@~/.vault_pass_dev \
  --vault-id prod@~/.vault_pass_prod
```

### 6.3 Vault 最佳实践

```yaml
# group_vars/production/vars.yaml — 明文变量引用加密变量
---
db_host: "db01.example.com"
db_port: 3306
db_user: "{{ vault_db_user }}"
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"

# group_vars/production/vault.yaml — 加密文件
---
vault_db_user: "admin"
vault_db_password: "SuperSecretPassword"
vault_api_key: "sk-xxxxxxxxxxxxxxxx"
```

---

## 7. Galaxy 与集合

### 7.1 Ansible Galaxy

```bash
# 搜索 Role
ansible-galaxy role search nginx

# 安装 Role
ansible-galaxy role install geerlingguy.docker
ansible-galaxy role install -r requirements.yaml

# 安装 Collection
ansible-galaxy collection install community.general
ansible-galaxy collection install -r requirements.yaml

# 列出已安装
ansible-galaxy role list
ansible-galaxy collection list
```

### 7.2 requirements.yaml

```yaml
---
# requirements.yaml
roles:
  - name: geerlingguy.docker
    version: "6.1.0"
  - name: geerlingguy.nginx
    version: "3.2.0"
  - name: my_private_role
    src: git+https://git.example.com/roles/my_role.git
    version: v1.0.0

collections:
  - name: community.general
    version: ">=7.0.0"
  - name: community.docker
    version: ">=3.0.0"
  - name: ansible.posix
    version: ">=1.5.0"
  - name: community.crypto
    version: ">=2.0.0"
```

### 7.3 创建自定义 Collection

```bash
# 初始化 Collection
ansible-galaxy collection init myorg.mytools

# 目录结构
myorg/mytools/
├── galaxy.yaml
├── plugins/
│   ├── modules/
│   ├── filter/
│   └── lookup/
├── roles/
├── playbooks/
└── docs/

# 构建与发布
ansible-galaxy collection build
ansible-galaxy collection publish myorg-mytools-1.0.0.tar.gz
```

---

## 8. AWX/Tower

### 8.1 AWX 部署（Docker Compose）

```bash
# 克隆 AWX
git clone https://github.com/ansible/awx.git
cd awx

# 使用 awx-operator（K8s 方式，推荐）
# 或使用 Docker Compose 方式
cd tools/docker-compose
make docker-compose-build
docker compose up -d
```

### 8.2 AWX 核心概念

```text
AWX/Tower 架构
├── Organization — 组织（多租户隔离）
├── Project — 项目（关联 Git 仓库的 Playbook）
├── Inventory — 主机清单（静态/动态/智能）
├── Credential — 凭证（SSH Key/Vault/Cloud API）
├── Template — 作业模板（Playbook + Inventory + Credential）
├── Workflow — 工作流（串联多个模板，支持条件分支）
├── Schedule — 定时调度
└── Notification — 通知（Slack/Email/Webhook）
```

### 8.3 AWX API 调用

```bash
# 获取 Token
TOKEN=$(curl -s -X POST "https://awx.example.com/api/v2/tokens/" \
  -u "admin:password" | jq -r '.token')

# 触发作业
curl -s -X POST "https://awx.example.com/api/v2/job_templates/1/launch/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"extra_vars": {"version": "2.1.0"}}'

# 查看作业状态
curl -s "https://awx.example.com/api/v2/jobs/42/" \
  -H "Authorization: Bearer $TOKEN" | jq '.status'
```

---

## 9. 性能优化

### 9.1 SSH 优化

```ini
# ansible.cfg
[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=300s -o PreferredAuthentications=publickey
control_path_dir = /tmp/.ansible-cp
```

### 9.2 Fact 缓存

```ini
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 7200
```

### 9.3 并行与异步

```yaml
# 提高并行度
# ansible.cfg: forks = 50

# 异步任务（长时间运行）
- name: 长时间编译任务
  command: /opt/build.sh
  async: 3600          # 最大运行时间（秒）
  poll: 0              # 不等待（fire-and-forget）
  register: build_job

- name: 检查编译状态
  async_status:
    jid: "{{ build_job.ansible_job_id }}"
  register: build_result
  until: build_result.finished
  retries: 60
  delay: 60

# 滚动更新
- name: 滚动部署
  hosts: webservers
  serial: "25%"        # 每批 25% 的主机
  max_fail_percentage: 10
  tasks:
    - name: 部署应用
      include_role:
        name: app_deploy
```

### 9.4 Mitogen 加速

```ini
# 安装 mitogen
# pip3 install mitogen

# ansible.cfg
[defaults]
strategy_plugins = /path/to/mitogen/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

---

## 10. 最佳实践

### 10.1 项目结构

```text
ansible-project/
├── ansible.cfg
├── requirements.yaml         # Galaxy 依赖
├── inventory/
│   ├── production/
│   │   ├── hosts.yaml
│   │   ├── group_vars/
│   │   └── host_vars/
│   └── staging/
│       ├── hosts.yaml
│       └── group_vars/
├── playbooks/
│   ├── site.yaml             # 主入口
│   ├── webservers.yaml
│   ├── dbservers.yaml
│   └── maintenance/
│       ├── rolling_update.yaml
│       └── backup.yaml
├── roles/
│   ├── common/
│   ├── nginx/
│   ├── mysql/
│   └── app_deploy/
├── templates/
├── files/
├── filter_plugins/
└── molecule/                 # 测试
    └── default/
        ├── molecule.yaml
        ├── converge.yaml
        └── verify.yaml
```

### 10.2 Ansible Lint

```bash
# 安装
pip3 install ansible-lint

# 运行检查
ansible-lint playbooks/

# 配置文件 .ansible-lint
---
skip_list:
  - yaml[line-length]
  - name[missing]
warn_list:
  - experimental
exclude_paths:
  - .cache/
  - .git/
```

### 10.3 Molecule 测试

```bash
# 安装
pip3 install molecule molecule-docker

# 初始化测试
cd roles/nginx
molecule init scenario --driver-name docker

# 运行测试
molecule test          # 完整测试流程
molecule converge      # 只运行 Playbook
molecule verify        # 只运行验证
molecule login         # 登录测试容器
molecule destroy       # 销毁测试环境
```

```yaml
# molecule/default/molecule.yaml
---
driver:
  name: docker
platforms:
  - name: ubuntu-jammy
    image: ubuntu:22.04
    pre_build_image: true
    privileged: true
    command: /lib/systemd/systemd
  - name: rocky-9
    image: rockylinux:9
    pre_build_image: true
    privileged: true
    command: /lib/systemd/systemd
provisioner:
  name: ansible
  playbooks:
    converge: converge.yaml
    verify: verify.yaml
verifier:
  name: ansible
```

---

## 11. 故障排查

### 11.1 常见问题

```bash
# SSH 连接失败
ansible all -m ping -vvvv  # 最详细输出

# 权限问题
# 确认 become 配置
ansible all -m command -a "whoami" --become

# 模块找不到
ansible-doc -l | grep module_name

# Playbook 语法检查
ansible-playbook playbooks/site.yaml --syntax-check

# 变量调试
- name: 打印变量
  debug:
    var: hostvars[inventory_hostname]

- name: 打印消息
  debug:
    msg: "当前主机: {{ inventory_hostname }}, IP: {{ ansible_default_ipv4.address }}"

# 执行日志
ANSIBLE_LOG_PATH=./ansible.log ansible-playbook site.yaml
```

### 11.2 调试技巧

```yaml
# 条件断点
- name: 暂停等待确认
  pause:
    prompt: "确认继续？(Ctrl+C 取消)"
  when: env == "production"

# 失败时输出详情
- name: 执行命令
  command: /opt/app/check.sh
  register: result
  failed_when: result.rc != 0

- name: 显示失败详情
  debug:
    var: result
  when: result is failed

# 策略控制
- name: 调试 Play
  hosts: all
  strategy: debug     # 失败时进入交互调试
  tasks:
    - name: 可能失败的任务
      command: /bin/false
```
