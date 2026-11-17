# Docker Compose 示例

## 单实例基础部署

```yaml
version: '3.8'

services:
  kingbase:
    image: kingbase:v1
    container_name: kingbase
    privileged: true
    restart: always
    ports:
      - "4321:54321"
    environment:
      - NEED_START=yes
      - DB_USER=system
      - DB_PASSWORD=12345678ab
      - DB_MODE=sqlserver
      - ENCODING=utf8
      - ENABLE_CI=yes
    volumes:
      - /opt/kingbase/data:/home/kingbase/userdata/
```

## 主从复制部署

```yaml
version: '3.8'

services:
  kingbase-primary:
    image: kingbase:v1
    container_name: kingbase-primary
    privileged: true
    restart: always
    ports:
      - "4321:54321"
    environment:
      - NEED_START=yes
      - DB_USER=system
      - DB_PASSWORD=12345678ab
      - DB_MODE=sqlserver
      - ENCODING=utf8
    volumes:
      - /opt/kingbase/primary:/home/kingbase/userdata/

  kingbase-standby:
    image: kingbase:v1
    container_name: kingbase-standby
    privileged: true
    restart: always
    ports:
      - "4322:54321"
    environment:
      - NEED_START=yes
      - DB_USER=system
      - DB_PASSWORD=12345678ab
      - DB_MODE=sqlserver
      - ENCODING=utf8
    volumes:
      - /opt/kingbase/standby:/home/kingbase/userdata/
    depends_on:
      - kingbase-primary
```

## 带外部网络配置

```yaml
version: '3.8'

services:
  kingbase:
    image: kingbase:v1
    container_name: kingbase
    privileged: true
    restart: always
    networks:
      - db-network
    ports:
      - "4321:54321"
    environment:
      - NEED_START=yes
      - DB_USER=system
      - DB_PASSWORD=12345678ab
      - DB_MODE=sqlserver
      - ENCODING=utf8
    volumes:
      - /opt/kingbase/data:/home/kingbase/userdata/

networks:
  db-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 多应用共享数据库

```yaml
version: '3.8'

services:
  kingbase:
    image: kingbase:v1
    container_name: kingbase
    privileged: true
    restart: always
    ports:
      - "4321:54321"
    environment:
      - NEED_START=yes
      - DB_USER=system
      - DB_PASSWORD=12345678ab
      - DB_MODE=sqlserver
      - ENCODING=utf8
    volumes:
      - /opt/kingbase/data:/home/kingbase/userdata/

  app-java:
    image: myapp-java:latest
    restart: always
    depends_on:
      - kingbase
    environment:
      - SPRING_DATASOURCE_URL=jdbc:kingbase8://kingbase:54321/test

  app-python:
    image: myapp-python:latest
    restart: always
    depends_on:
      - kingbase
    environment:
      - DATABASE_URL=kingbase://system:12345678ab@kingbase:54321/test
```

## 注意事项

1. 数据挂载目录权限必须为 755
2. Docker 环境需申请专门的 Docker 版 License
3. 容器内数据库端口固定为 54321
4. 配置文件修改后需执行 `sys_ctl reload`
