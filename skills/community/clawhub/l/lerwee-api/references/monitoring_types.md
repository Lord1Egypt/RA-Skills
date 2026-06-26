# Monitoring Types Reference

乐维监控平台监控类型对照表。

## 监控分类 (Classification)

| 值 | 分类名称 | 说明 |
|----|----------|------|
| 101 | 系统监控 | Linux、Windows、AIX 等操作系统监控 |
| 102 | 网络设备 | 路由器、交换机、防火墙等网络设备 |
| 103 | 存储设备 | SAN、NAS 等存储设备 |
| 104 | 数据库 | MySQL、Oracle、SQL Server 等 |
| 105 | 中间件 | Tomcat、WebLogic、WebSphere 等 |
| 106 | 应用服务 | HTTP、HTTPS 等应用服务监控 |
| 107 | 虚拟化 | VMware、KVM、Xen 等虚拟化平台 |
| 108 | 云平台 | OpenStack、Kubernetes、Docker |
| 109 | 硬件设备 | 服务器硬件、IPMI 等 |
| 110 | 自定义 | 自定义监控类型 |

## 系统监控子类型 (Subtype - 101)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 101001 | Linux | Linux 操作系统 |
| 101002 | Windows | Windows 操作系统 |
| 101003 | AIX | IBM AIX 操作系统 |
| 101004 | Solaris | Oracle Solaris 操作系统 |
| 101005 | HP-UX | HP-UX 操作系统 |

## 网络设备子类型 (Subtype - 102)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 102001 | 路由器 | 各类路由器设备 |
| 102002 | 交换机 | 各类交换机设备 |
| 102003 | 防火墙 | 各类防火墙设备 |
| 102004 | 负载均衡 | F5、Nginx 等负载均衡设备 |
| 102005 | 无线AP | 无线接入点 |

## 存储设备子类型 (Subtype - 103)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 103001 | SAN | 存储区域网络 |
| 103002 | NAS | 网络附加存储 |
| 103003 | 存储 | 其他存储设备 |

## 数据库子类型 (Subtype - 104)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 104001 | MySQL | MySQL 数据库 |
| 104002 | Oracle | Oracle 数据库 |
| 104003 | SQL Server | Microsoft SQL Server |
| 104004 | PostgreSQL | PostgreSQL 数据库 |
| 104005 | Redis | Redis 缓存数据库 |
| 104006 | MongoDB | MongoDB 文档数据库 |
| 104007 | DB2 | IBM DB2 数据库 |

## 中间件子类型 (Subtype - 105)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 105001 | Tomcat | Apache Tomcat |
| 105002 | WebLogic | Oracle WebLogic |
| 105003 | WebSphere | IBM WebSphere |
| 105004 | JBoss | Red Hat JBoss |
| 105005 | Jetty | Eclipse Jetty |
| 105006 | Nginx | Nginx Web Server |

## 应用服务子类型 (Subtype - 106)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 106001 | HTTP | HTTP 服务监控 |
| 106002 | HTTPS | HTTPS 服务监控 |
| 106003 | TCP | TCP 端口监控 |
| 106004 | UDP | UDP 端口监控 |
| 106005 | ICMP | Ping 监控 |
| 106006 | FTP | FTP 服务监控 |
| 106007 | DNS | DNS 服务监控 |
| 106008 | SMTP | SMTP 邮件服务监控 |
| 106009 | POP3 | POP3 邮件服务监控 |
| 106010 | IMAP | IMAP 邮件服务监控 |

## 虚拟化子类型 (Subtype - 107)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 107001 | VMware | VMware vCenter/ESXi |
| 107002 | KVM | KVM 虚拟化 |
| 107003 | Xen | Xen 虚拟化 |
| 107004 | Hyper-V | Microsoft Hyper-V |

## 云平台子类型 (Subtype - 108)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 108001 | OpenStack | OpenStack 云平台 |
| 108002 | Kubernetes | Kubernetes 容器编排 |
| 108003 | Docker | Docker 容器 |
| 108004 | AWS | Amazon Web Services |
| 108005 | Azure | Microsoft Azure |
| 108006 | Aliyun | 阿里云 |

## 硬件设备子类型 (Subtype - 109)

| 值 | 子类型名称 | 说明 |
|----|-----------|------|
| 109001 | IPMI | IPMI 硬件监控 |
| 109002 | 服务器 | 服务器硬件 |
| 109003 | 机柜 | 机柜设备 |

## 监控状态 (Active Status)

| 值 | 状态名称 | 说明 |
|----|----------|------|
| -1 | 未监控 | 对象未启用监控 |
| 0 | 正常 | 监控正常，无告警 |
| 1 | 信息 | 信息级别告警 |
| 2 | 警告 | 警告级别告警 |
| 3 | 一般严重 | 一般严重级别告警 |
| 4 | 严重 | 严重级别告警 |
| 5 | 致命 | 致命级别告警 |

## 采集状态 (Power Status)

| 值 | 状态名称 | 说明 |
|----|----------|------|
| 1 | 正常 | 数据采集正常 |
| 2 | 异常 | 数据采集异常 |

## 告警等级 (Alarm Level)

| 值 | 等级名称 | 说明 |
|----|----------|------|
| 1 | 信息 | 信息级别 |
| 2 | 警告 | 警告级别 |
| 3 | 一般 | 一般严重 |
| 4 | 严重 | 严重级别 |
| 5 | 致命 | 致命级别 |

## 告警状态 (Alarm Status)

| 值 | 状态名称 | 说明 |
|----|----------|------|
| 0 | 待处理 | 告警未处理 |
| 1 | 处理中 | 告警正在处理 |
| 2 | 已处理 | 告警已处理/关闭 |
