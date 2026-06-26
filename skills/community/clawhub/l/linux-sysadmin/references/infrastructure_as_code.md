# 基础设施即代码（IaC）参考文档

> 覆盖 Terraform、Packer、Cloud-Init、Vagrant、GitOps 工作流、IaC 最佳实践与多云管理。

---

## 目录

- [1. IaC 概述](#1-iac-概述)
- [2. Terraform 基础](#2-terraform-基础)
- [3. Terraform 进阶](#3-terraform-进阶)
- [4. Terraform 状态管理](#4-terraform-状态管理)
- [5. Terraform 模块](#5-terraform-模块)
- [6. Packer 镜像构建](#6-packer-镜像构建)
- [7. Cloud-Init](#7-cloud-init)
- [8. Vagrant](#8-vagrant)
- [9. GitOps 工作流](#9-gitops-工作流)
- [10. IaC 安全](#10-iac-安全)
- [11. 多云管理](#11-多云管理)
- [12. 最佳实践](#12-最佳实践)

---

## 1. IaC 概述

### 1.1 核心理念

```text
IaC（Infrastructure as Code）核心原则
├── 声明式定义 — 描述"期望状态"，工具自动实现
├── 版本控制 — 所有基础设施配置纳入 Git 管理
├── 幂等性 — 多次执行结果相同
├── 可重复 — 任何环境都能从代码重建
├── 自文档化 — 代码即文档，配置即说明
└── 可审计 — 所有变更有记录、可追溯

IaC 工具分类
├── 编排工具（Orchestration）
│   ├── Terraform — 多云资源编排（声明式，HCL）
│   ├── Pulumi — 多云编排（通用编程语言）
│   └── CloudFormation — AWS 专用
├── 配置管理（Configuration Management）
│   ├── Ansible — 无 Agent，SSH 推送
│   ├── Puppet — Agent 拉取，声明式
│   ├── Chef — Agent 拉取，命令式（Ruby DSL）
│   └── Salt — 支持推/拉模式
├── 镜像构建（Image Building）
│   ├── Packer — 多平台机器镜像
│   └── Docker — 容器镜像
├── 初始化（Bootstrapping）
│   ├── Cloud-Init — 云实例首次启动配置
│   └── Ignition — CoreOS/Flatcar 初始化
└── 开发环境（Development）
    ├── Vagrant — 本地虚拟机管理
    └── DevContainers — 容器化开发环境
```

### 1.2 IaC 工作流

```text
开发流程
  编写代码 → Lint/Validate → Plan → Code Review → Apply → 验证 → 监控

CI/CD 集成
  Git Push → Pipeline 触发 → terraform fmt/validate → terraform plan →
  → MR 评审（plan 输出作为评论）→ 合并到 main → terraform apply → 通知
```

---

## 2. Terraform 基础

### 2.1 安装与配置

```bash
# 安装 Terraform
wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip
unzip terraform_1.7.0_linux_amd64.zip
mv terraform /usr/local/bin/
terraform version

# 安装 tfenv（版本管理，推荐）
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
tfenv install 1.7.0
tfenv use 1.7.0

# 配置 Provider 镜像（国内加速）
cat > ~/.terraformrc << 'EOF'
provider_installation {
  network_mirror {
    url = "https://mirrors.tencent.com/terraform/"
  }
}
EOF
```

### 2.2 基本概念

```hcl
# main.tf — Terraform 配置文件

# Provider 配置
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    tencentcloud = {
      source  = "tencentcloudstack/tencentcloud"
      version = "~> 1.81"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # 远程状态存储
  backend "cos" {
    region = "ap-guangzhou"
    bucket = "terraform-state-xxxxx"
    prefix = "myproject"
  }
}

# Provider 认证
provider "tencentcloud" {
  region     = var.region
  secret_id  = var.secret_id
  secret_key = var.secret_key
}

provider "aws" {
  region = "ap-southeast-1"
}
```

### 2.3 资源定义

```hcl
# variables.tf — 变量定义
variable "region" {
  description = "部署区域"
  type        = string
  default     = "ap-guangzhou"
}

variable "instance_type" {
  description = "实例规格"
  type        = string
  default     = "S5.MEDIUM4"
}

variable "instance_count" {
  description = "实例数量"
  type        = number
  default     = 2
  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "实例数量必须在 1-10 之间"
  }
}

variable "tags" {
  description = "资源标签"
  type        = map(string)
  default = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "myproject"
  }
}

# 敏感变量
variable "secret_id" {
  type      = string
  sensitive = true
}

variable "secret_key" {
  type      = string
  sensitive = true
}
```

```hcl
# resources.tf — 资源定义

# VPC
resource "tencentcloud_vpc" "main" {
  name       = "${var.project}-vpc"
  cidr_block = "10.0.0.0/16"
  tags       = var.tags
}

# 子网
resource "tencentcloud_subnet" "web" {
  count             = 2
  name              = "${var.project}-web-${count.index + 1}"
  vpc_id            = tencentcloud_vpc.main.id
  cidr_block        = cidrsubnet("10.0.0.0/16", 8, count.index)
  availability_zone = var.availability_zones[count.index]
  tags              = var.tags
}

# 安全组
resource "tencentcloud_security_group" "web" {
  name        = "${var.project}-web-sg"
  description = "Web server security group"
  tags        = var.tags
}

resource "tencentcloud_security_group_lite_rule" "web" {
  security_group_id = tencentcloud_security_group.web.id

  ingress = [
    "ACCEPT#0.0.0.0/0#80#TCP",
    "ACCEPT#0.0.0.0/0#443#TCP",
    "ACCEPT#10.0.0.0/16#22#TCP",
  ]

  egress = [
    "ACCEPT#0.0.0.0/0#ALL#ALL",
  ]
}

# CVM 实例
resource "tencentcloud_instance" "web" {
  count         = var.instance_count
  instance_name = "${var.project}-web-${count.index + 1}"
  instance_type = var.instance_type
  image_id      = data.tencentcloud_images.ubuntu.images[0].image_id

  vpc_id    = tencentcloud_vpc.main.id
  subnet_id = tencentcloud_subnet.web[count.index % length(tencentcloud_subnet.web)].id

  system_disk_type = "CLOUD_PREMIUM"
  system_disk_size = 50

  orderly_security_groups = [tencentcloud_security_group.web.id]

  user_data = base64encode(templatefile("${path.module}/scripts/init.sh", {
    hostname = "${var.project}-web-${count.index + 1}"
    env      = var.environment
  }))

  tags = merge(var.tags, {
    Name = "${var.project}-web-${count.index + 1}"
    Role = "web"
  })
}

# 数据源
data "tencentcloud_images" "ubuntu" {
  image_type = ["PUBLIC_IMAGE"]
  os_name    = "Ubuntu Server 22.04"
}

data "tencentcloud_availability_zones" "zones" {}
```

```hcl
# outputs.tf — 输出定义
output "vpc_id" {
  description = "VPC ID"
  value       = tencentcloud_vpc.main.id
}

output "instance_ips" {
  description = "实例私网 IP 列表"
  value       = tencentcloud_instance.web[*].private_ip
}

output "instance_ids" {
  description = "实例 ID 列表"
  value       = tencentcloud_instance.web[*].id
}

output "lb_public_ip" {
  description = "负载均衡公网 IP"
  value       = tencentcloud_clb_instance.web.clb_vips[0]
  sensitive   = false
}
```

### 2.4 基本命令

```bash
# 初始化（下载 Provider）
terraform init
terraform init -upgrade          # 更新 Provider

# 格式化
terraform fmt -recursive

# 验证
terraform validate

# 计划（预览变更）
terraform plan
terraform plan -out=tfplan       # 保存 plan
terraform plan -target=tencentcloud_instance.web[0]  # 只针对特定资源

# 应用
terraform apply
terraform apply tfplan           # 应用已保存的 plan
terraform apply -auto-approve    # 跳过确认（CI/CD 用）

# 销毁
terraform destroy
terraform destroy -target=tencentcloud_instance.web[0]

# 查看状态
terraform show
terraform state list
terraform state show tencentcloud_instance.web[0]

# 导入已有资源
terraform import tencentcloud_instance.web[0] ins-xxxxxxxx

# 输出值
terraform output
terraform output -json instance_ips
```

---

## 3. Terraform 进阶

### 3.1 条件与循环

```hcl
# 条件表达式
resource "tencentcloud_eip" "web" {
  count = var.create_eip ? var.instance_count : 0
  name  = "${var.project}-eip-${count.index + 1}"
  type  = "EIP"
}

# for_each（推荐替代 count）
variable "instances" {
  type = map(object({
    type    = string
    subnet  = string
    role    = string
  }))
  default = {
    "web-1" = { type = "S5.MEDIUM4", subnet = "web", role = "web" }
    "web-2" = { type = "S5.MEDIUM4", subnet = "web", role = "web" }
    "db-1"  = { type = "S5.LARGE8",  subnet = "db",  role = "db" }
  }
}

resource "tencentcloud_instance" "servers" {
  for_each      = var.instances
  instance_name = "${var.project}-${each.key}"
  instance_type = each.value.type
  # ...
}

# for 表达式
output "instance_map" {
  value = {
    for k, v in tencentcloud_instance.servers :
    k => v.private_ip
  }
}

# dynamic 块
resource "tencentcloud_security_group_lite_rule" "dynamic" {
  security_group_id = tencentcloud_security_group.web.id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      # ...
    }
  }
}
```

### 3.2 数据源与 Provisioner

```hcl
# 数据源（查询已有资源）
data "tencentcloud_vpc_subnets" "existing" {
  vpc_id = "vpc-xxxxxxxx"
}

# 本地文件
data "local_file" "ssh_key" {
  filename = "${path.module}/keys/id_ed25519.pub"
}

# Provisioner（最后手段，优先用 Cloud-Init/Ansible）
resource "tencentcloud_instance" "web" {
  # ...

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_ed25519")
      host        = self.private_ip
    }
  }

  provisioner "local-exec" {
    command = "ansible-playbook -i '${self.private_ip},' playbooks/configure.yaml"
  }
}
```

### 3.3 Lifecycle 管理

```hcl
resource "tencentcloud_instance" "web" {
  # ...

  lifecycle {
    create_before_destroy = true   # 先创建新实例再销毁旧实例
    prevent_destroy       = true   # 防止意外删除
    ignore_changes        = [      # 忽略外部变更
      tags,
      user_data,
    ]
  }
}

# 移动资源（重构时避免销毁重建）
moved {
  from = tencentcloud_instance.web
  to   = module.compute.tencentcloud_instance.web
}
```

---

## 4. Terraform 状态管理

### 4.1 远程状态后端

```hcl
# 腾讯云 COS 后端
terraform {
  backend "cos" {
    region = "ap-guangzhou"
    bucket = "terraform-state-xxxxx"
    prefix = "myproject/production"
    encrypt = true
  }
}

# AWS S3 后端
terraform {
  backend "s3" {
    bucket         = "terraform-state-xxxxx"
    key            = "myproject/production/terraform.tfstate"
    region         = "ap-southeast-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# HTTP 后端（GitLab/自建）
terraform {
  backend "http" {
    address        = "https://gitlab.example.com/api/v4/projects/1/terraform/state/production"
    lock_address   = "https://gitlab.example.com/api/v4/projects/1/terraform/state/production/lock"
    unlock_address = "https://gitlab.example.com/api/v4/projects/1/terraform/state/production/lock"
    username       = "gitlab-ci-token"
    password       = "glpat-xxxxxxxxxx"
  }
}
```

### 4.2 状态操作

```bash
# 列出资源
terraform state list

# 查看资源详情
terraform state show tencentcloud_instance.web[0]

# 移动资源（重命名）
terraform state mv tencentcloud_instance.web tencentcloud_instance.webserver

# 移除资源（不销毁实际资源）
terraform state rm tencentcloud_instance.web[0]

# 拉取远程状态
terraform state pull > state.json

# 推送状态（危险操作）
terraform state push state.json

# 标记资源需要重建
terraform taint tencentcloud_instance.web[0]    # 已废弃
terraform apply -replace=tencentcloud_instance.web[0]  # 推荐
```

### 4.3 Workspace

```bash
# 工作空间管理（环境隔离）
terraform workspace list
terraform workspace new staging
terraform workspace new production
terraform workspace select staging
terraform workspace show

# 在配置中使用 workspace
resource "tencentcloud_instance" "web" {
  instance_name = "${var.project}-${terraform.workspace}-web"
  # ...
}
```

---

## 5. Terraform 模块

### 5.1 模块结构

```text
modules/
└── compute/
    ├── main.tf          # 资源定义
    ├── variables.tf     # 输入变量
    ├── outputs.tf       # 输出值
    ├── versions.tf      # Provider 版本约束
    └── README.md        # 使用文档
```

### 5.2 模块定义

```hcl
# modules/compute/variables.tf
variable "project" {
  type = string
}

variable "instance_count" {
  type    = number
  default = 1
}

variable "instance_type" {
  type    = string
  default = "S5.MEDIUM4"
}

variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_ids" {
  type = list(string)
}

# modules/compute/main.tf
resource "tencentcloud_instance" "this" {
  count         = var.instance_count
  instance_name = "${var.project}-${count.index + 1}"
  instance_type = var.instance_type
  vpc_id        = var.vpc_id
  subnet_id     = var.subnet_ids[count.index % length(var.subnet_ids)]
  orderly_security_groups = var.security_group_ids
  # ...
}

# modules/compute/outputs.tf
output "instance_ids" {
  value = tencentcloud_instance.this[*].id
}

output "private_ips" {
  value = tencentcloud_instance.this[*].private_ip
}
```

### 5.3 模块调用

```hcl
# 根模块调用子模块
module "web_servers" {
  source = "./modules/compute"

  project            = var.project
  instance_count     = 3
  instance_type      = "S5.MEDIUM4"
  vpc_id             = module.network.vpc_id
  subnet_ids         = module.network.web_subnet_ids
  security_group_ids = [module.security.web_sg_id]
}

module "db_servers" {
  source = "./modules/compute"

  project            = var.project
  instance_count     = 2
  instance_type      = "S5.LARGE8"
  vpc_id             = module.network.vpc_id
  subnet_ids         = module.network.db_subnet_ids
  security_group_ids = [module.security.db_sg_id]
}

# 使用远程模块
module "vpc" {
  source  = "terraform-tencentcloud-modules/vpc/tencentcloud"
  version = "~> 1.0"
  # ...
}
```

---

## 6. Packer 镜像构建

### 6.1 基本使用

```bash
# 安装
wget https://releases.hashicorp.com/packer/1.10.0/packer_1.10.0_linux_amd64.zip
unzip packer_1.10.0_linux_amd64.zip
mv packer /usr/local/bin/

# 验证
packer version
```

### 6.2 Packer 模板（HCL2）

```hcl
# image.pkr.hcl
packer {
  required_plugins {
    tencentcloud = {
      source  = "github.com/tencentcloudstack/tencentcloud"
      version = ">= 1.0.0"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = ">= 1.1.0"
    }
  }
}

variable "region" {
  type    = string
  default = "ap-guangzhou"
}

source "tencentcloud-cvm" "ubuntu" {
  region       = var.region
  zone         = "${var.region}-3"
  instance_type = "S5.MEDIUM4"
  source_image_id = "img-xxxxxxxx"

  image_name        = "myapp-base-{{timestamp}}"
  image_description = "Base image with common packages"

  ssh_username = "ubuntu"
}

build {
  sources = ["source.tencentcloud-cvm.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y curl wget vim htop",
    ]
  }

  provisioner "ansible" {
    playbook_file = "./ansible/configure.yaml"
    extra_arguments = [
      "--extra-vars", "env=production"
    ]
  }

  provisioner "shell" {
    inline = [
      "sudo apt-get clean",
      "sudo rm -rf /var/lib/apt/lists/*",
      "sudo rm -rf /tmp/*",
    ]
  }

  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
```

### 6.3 Packer 命令

```bash
# 初始化（下载插件）
packer init .

# 验证模板
packer validate .

# 格式化
packer fmt .

# 构建镜像
packer build .
packer build -var "region=ap-shanghai" .
packer build -only="tencentcloud-cvm.ubuntu" .

# 调试模式
packer build -debug .
```

---

## 7. Cloud-Init

### 7.1 基本配置

```yaml
#cloud-config
# cloud-init 配置（首次启动时执行）

# 设置主机名
hostname: web-server-01
fqdn: web-server-01.example.com
manage_etc_hosts: true

# 设置时区
timezone: Asia/Shanghai

# 创建用户
users:
  - name: deploy
    groups: sudo, docker
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... deploy@example.com
    lock_passwd: true

# 安装软件包
package_update: true
package_upgrade: true
packages:
  - curl
  - wget
  - vim
  - htop
  - docker.io
  - nginx
  - python3-pip
  - fail2ban
  - unattended-upgrades

# 写入文件
write_files:
  - path: /etc/nginx/sites-available/default
    content: |
      server {
          listen 80;
          server_name _;
          root /var/www/html;
          index index.html;
      }
    owner: root:root
    permissions: '0644'

  - path: /etc/sysctl.d/99-custom.conf
    content: |
      net.core.somaxconn = 65535
      net.ipv4.tcp_max_syn_backlog = 65535
      vm.swappiness = 10
    owner: root:root
    permissions: '0644'

# 执行命令
runcmd:
  - systemctl enable --now docker
  - systemctl enable --now nginx
  - sysctl --system
  - usermod -aG docker deploy
  # 安装 Node Exporter
  - |
    wget -q https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
    tar xzf node_exporter-1.8.2.linux-amd64.tar.gz
    cp node_exporter-1.8.2.linux-amd64/node_exporter /usr/local/bin/
    useradd -rs /bin/false node_exporter
    cat > /etc/systemd/system/node_exporter.service << 'UNIT'
    [Unit]
    Description=Node Exporter
    After=network.target
    [Service]
    User=node_exporter
    ExecStart=/usr/local/bin/node_exporter
    [Install]
    WantedBy=multi-user.target
    UNIT
    systemctl daemon-reload
    systemctl enable --now node_exporter

# 最终消息
final_message: "Cloud-init 完成，耗时 $UPTIME 秒"

# 关闭后操作
power_state:
  mode: reboot
  message: "Cloud-init 配置完成，重启中..."
  timeout: 30
  condition: true
```

### 7.2 Cloud-Init 调试

```bash
# 查看 Cloud-Init 状态
cloud-init status
cloud-init status --long

# 查看日志
cat /var/log/cloud-init.log
cat /var/log/cloud-init-output.log

# 重新运行
sudo cloud-init clean --logs
sudo cloud-init init
sudo cloud-init modules --mode=config
sudo cloud-init modules --mode=final

# 验证配置
cloud-init schema --config-file userdata.yaml
```

---

## 8. Vagrant

### 8.1 基本使用

```bash
# 安装
# 下载：https://www.vagrantup.com/downloads
# 需要 VirtualBox、libvirt 或 Docker 作为 Provider

# 初始化
vagrant init ubuntu/jammy64
vagrant init generic/rocky9

# 常用命令
vagrant up              # 启动虚拟机
vagrant ssh             # SSH 登录
vagrant halt            # 关机
vagrant reload          # 重启（重新加载 Vagrantfile）
vagrant destroy         # 销毁
vagrant status          # 查看状态
vagrant snapshot save   # 快照
```

### 8.2 Vagrantfile

```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  # 全局配置
  config.vm.box = "ubuntu/jammy64"
  config.vm.box_check_update = false

  # Web 服务器
  config.vm.define "web" do |web|
    web.vm.hostname = "web-server"
    web.vm.network "private_network", ip: "10.0.1.10"
    web.vm.network "forwarded_port", guest: 80, host: 8080

    web.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2
      vb.name = "web-server"
    end

    web.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y nginx
      systemctl enable --now nginx
    SHELL

    web.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbooks/web.yaml"
    end
  end

  # 数据库服务器
  config.vm.define "db" do |db|
    db.vm.hostname = "db-server"
    db.vm.network "private_network", ip: "192.168.56.11"

    db.vm.provider "virtualbox" do |vb|
      vb.memory = 4096
      vb.cpus = 2
    end

    db.vm.provision "shell", path: "scripts/setup_db.sh"
  end

  # 同步目录
  config.vm.synced_folder "./app", "/opt/app"
end
```

### 8.3 多机编排

```ruby
# 批量创建
Vagrant.configure("2") do |config|
  (1..3).each do |i|
    config.vm.define "node-#{i}" do |node|
      node.vm.box = "ubuntu/jammy64"
      node.vm.hostname = "node-#{i}"
      node.vm.network "private_network", ip: "192.168.56.#{10 + i}"

      node.vm.provider "virtualbox" do |vb|
        vb.memory = 2048
        vb.cpus = 2
      end

      # 最后一台执行 Ansible（一次性配置所有）
      if i == 3
        node.vm.provision "ansible" do |ansible|
          ansible.limit = "all"
          ansible.playbook = "playbooks/cluster.yaml"
          ansible.groups = {
            "nodes" => ["node-1", "node-2", "node-3"],
          }
        end
      end
    end
  end
end
```

---

## 9. GitOps 工作流

### 9.1 GitOps 原则

```text
GitOps 核心原则
├── 声明式 — 系统状态以声明式方式描述
├── 版本化 — 所有配置存储在 Git 仓库
├── 自动化 — 变更自动应用（Push/Pull 模式）
├── 可观测 — 实际状态与期望状态持续对比
└── 自愈 — 检测到偏差时自动修复

GitOps 工具
├── ArgoCD — K8s GitOps 控制器（Pull 模式）
├── Flux — K8s GitOps 工具包
├── Atlantis — Terraform Pull Request 自动化
└── Spacelift — Terraform CI/CD 平台
```

### 9.2 Atlantis（Terraform GitOps）

```yaml
# atlantis.yaml（仓库级配置）
version: 3
projects:
  - name: production
    dir: envs/production
    workspace: default
    terraform_version: v1.7.0
    autoplan:
      when_modified:
        - "*.tf"
        - "../modules/**/*.tf"
      enabled: true
    apply_requirements:
      - approved
      - mergeable
    workflow: custom

  - name: staging
    dir: envs/staging
    workspace: default
    terraform_version: v1.7.0
    autoplan:
      enabled: true

workflows:
  custom:
    plan:
      steps:
        - init:
            extra_args: ["-upgrade"]
        - run: terraform fmt -check -recursive
        - run: terraform validate
        - plan:
            extra_args: ["-var-file=terraform.tfvars"]
    apply:
      steps:
        - apply:
            extra_args: ["-var-file=terraform.tfvars"]
```

### 9.3 CI/CD Pipeline 示例

```yaml
# .gitlab-ci.yml — Terraform CI/CD
stages:
  - validate
  - plan
  - apply

variables:
  TF_DIR: "envs/production"

.terraform_base:
  image: hashicorp/terraform:1.7
  before_script:
    - cd $TF_DIR
    - terraform init -backend-config="key=${CI_PROJECT_NAME}/${CI_ENVIRONMENT_NAME}"

validate:
  extends: .terraform_base
  stage: validate
  script:
    - terraform fmt -check -recursive
    - terraform validate
  rules:
    - if: $CI_MERGE_REQUEST_ID

plan:
  extends: .terraform_base
  stage: plan
  script:
    - terraform plan -out=tfplan
    - terraform show -no-color tfplan > plan.txt
  artifacts:
    paths:
      - ${TF_DIR}/tfplan
      - ${TF_DIR}/plan.txt
  rules:
    - if: $CI_MERGE_REQUEST_ID

apply:
  extends: .terraform_base
  stage: apply
  script:
    - terraform apply -auto-approve tfplan
  dependencies:
    - plan
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
  environment:
    name: production
```

---

## 10. IaC 安全

### 10.1 敏感信息管理

```bash
# 使用环境变量
export TF_VAR_secret_id="AKIDxxxxxxxxxx"
export TF_VAR_secret_key="xxxxxxxxxxxxxxxx"

# 使用 .tfvars 文件（不要提交到 Git）
# terraform.tfvars
secret_id  = "AKIDxxxxxxxxxx"
secret_key = "xxxxxxxxxxxxxxxx"

# .gitignore
*.tfvars
*.tfstate
*.tfstate.backup
.terraform/
```

### 10.2 安全扫描

```bash
# tfsec — Terraform 安全扫描
tfsec .
tfsec --format json .

# checkov — 多框架安全扫描
checkov -d .
checkov --framework terraform -d .

# terrascan — 合规性检查
terrascan scan -t aws -i terraform

# OPA/Conftest — 策略即代码
conftest test . --policy policy/
```

### 10.3 最小权限

```hcl
# 为 Terraform 创建最小权限的 IAM 角色
# 只授予管理目标资源所需的权限
# 使用 Terraform state 的只读/读写分离
# CI/CD pipeline 中使用临时凭证（STS）
```

---

## 11. 多云管理

### 11.1 多 Provider 配置

```hcl
# 多云部署
provider "tencentcloud" {
  alias  = "guangzhou"
  region = "ap-guangzhou"
}

provider "tencentcloud" {
  alias  = "shanghai"
  region = "ap-shanghai"
}

provider "aws" {
  alias  = "singapore"
  region = "ap-southeast-1"
}

# 使用别名
resource "tencentcloud_instance" "gz_web" {
  provider = tencentcloud.guangzhou
  # ...
}

resource "tencentcloud_instance" "sh_web" {
  provider = tencentcloud.shanghai
  # ...
}
```

### 11.2 Terragrunt（DRY 配置）

```hcl
# terragrunt.hcl — 根配置
remote_state {
  backend = "cos"
  config = {
    region = "ap-guangzhou"
    bucket = "terraform-state-xxxxx"
    prefix = "${path_relative_to_include()}"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite"
  contents  = <<EOF
provider "tencentcloud" {
  region = var.region
}
EOF
}

# envs/production/web/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules//compute"
}

inputs = {
  project        = "myproject"
  environment    = "production"
  instance_count = 3
  instance_type  = "S5.MEDIUM4"
}
```

---

## 12. 最佳实践

### 12.1 项目结构

```text
terraform-project/
├── modules/                    # 可复用模块
│   ├── compute/
│   ├── network/
│   ├── security/
│   └── database/
├── envs/                       # 环境配置
│   ├── production/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── staging/
│       ├── main.tf
│       └── terraform.tfvars
├── scripts/                    # 辅助脚本
│   ├── init.sh
│   └── validate.sh
├── policy/                     # OPA 策略
│   └── terraform.rego
├── .gitignore
├── .pre-commit-config.yaml
└── README.md
```

### 12.2 命名规范

```hcl
# 资源命名：项目-环境-角色-编号
# 例如：myproject-prod-web-01

# Terraform 资源名使用下划线
resource "tencentcloud_instance" "web_server" {}

# 变量名使用下划线
variable "instance_type" {}

# 输出名使用下划线
output "vpc_id" {}

# 标签统一
tags = {
  Project     = "myproject"
  Environment = "production"
  ManagedBy   = "terraform"
  Team        = "platform"
  CostCenter  = "IT-001"
}
```

### 12.3 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.88.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_docs
        args:
          - --hook-config=--path-to-file=README.md
      - id: terraform_tflint
      - id: terraform_tfsec
      - id: terraform_checkov
```

```bash
# 安装并运行
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
