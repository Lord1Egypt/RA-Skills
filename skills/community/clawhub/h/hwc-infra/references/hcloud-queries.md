# KooCLI (hcloud) 常用命令

## 目录
- [ECS - 弹性云服务器](#ecs---弹性云服务器)
- [VPC - 虚拟私有云](#vpc---虚拟私有云)
- [RDS - 关系型数据库服务](#rds---关系型数据库服务)
- [写操作](#写操作执行前需确认)

---

## ECS - 弹性云服务器
```bash
# 实例列表
hcloud ECS ListServersDetails --cli-query='servers[].[id,name,status,flavor.name]'

# 实例详情
hcloud ECS ShowServer --server_id <id>

# 规格列表
hcloud ECS ListFlavors

# 镜像列表
hcloud ECS ListImagesDetails
```

## VPC - 虚拟私有云
```bash
# VPC 列表
hcloud VPC ListVpcs --cli-query='vpcs[].[id,name,cidr,status]'

# VPC 详情
hcloud VPC ShowVpc --vpc_id <id>

# 子网列表
hcloud VPC ListSubnets

# 安全组列表
hcloud VPC ListSecurityGroups

# 安全组规则
hcloud VPC ShowSecurityGroup --security_group_id <id>
```

## RDS - 关系型数据库服务
```bash
# 实例列表
hcloud RDS ListInstances --cli-query='instances[].[id,name,status,datastore.type]'

# 实例详情
hcloud RDS ShowInstance --instance_id <id>

# 规格列表
hcloud RDS ListFlavors --database_type MySQL

# 备份列表
hcloud RDS ListBackups --instance_id <id>
```

## 写操作（执行前需确认）
```bash
# ECS 操作
hcloud ECS BatchStartServers --os-start.body='[{"id":"<id>"}]'
hcloud ECS BatchStopServers --os-stop.body='[{"id":"<id>"}]'
hcloud ECS BatchRebootServers --os-reboot.body='[{"id":"<id>"}]'
hcloud ECS DeleteServer --server_id <id>

# RDS 操作
hcloud RDS RestartInstance --instance_id <id>
hcloud RDS DeleteInstance --instance_id <id>
```
