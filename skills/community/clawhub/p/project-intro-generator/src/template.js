const { THEMES } = require('./themes');

const DEP_USAGE = [
  { key: 'express', note: 'Node.js Web应用' },
  { key: 'koa', note: 'Node.js 轻量Web' },
  { key: 'nest', note: 'Node.js 企业级Web' },
  { key: 'fastify', note: '高性能 Node.js Web' },
  { key: 'hapi', note: 'Node.js Web' },
  { key: 'sails', note: 'Node.js MVC' },
  { key: 'adonis', note: 'Node.js 全栈Web' },
  { key: 'strapi', note: '无头 CMS' },
  { key: 'loopback', note: 'API' },
  { key: 'feathers', note: '实时 API' },
  { key: 'moleculer', note: '微服务' },
  { key: 'restify', note: 'REST API' },
  { key: 'egg', note: 'Node.js 企业级' },
  { key: 'midway', note: 'Node.js 全栈' },
  { key: 'meteor', note: '全栈 JS' },
  { key: 'django', note: 'Python Web' },
  { key: 'flask', note: 'Python 轻量Web' },
  { key: 'fastapi', note: '高性能 Python Web' },
  { key: 'bottle', note: 'Python 微Web' },
  { key: 'tornado', note: '异步 Python Web' },
  { key: 'sanic', note: '异步 Python Web' },
  { key: 'pyramid', note: 'Python Web' },
  { key: 'falcon', note: '轻量 Python API' },
  { key: 'aiohttp', note: '异步 Python HTTP' },
  { key: 'web2py', note: 'Python 全栈Web' },
  { key: 'requests', note: 'HTTP客户端' },
  { key: 'httpx', note: 'HTTP客户端' },
  { key: 'urllib3', note: 'HTTP库' },
  { key: 'yagmail', note: '邮件发送' },
  { key: 'sendgrid', note: '邮件发送' },
  { key: 'boto3', note: '对象存储' },
  { key: 'minio', note: '对象存储' },
  { key: 'google-cloud-storage', note: '对象存储' },
  { key: 'sqlalchemy', note: 'ORM' },
  { key: 'drf', note: 'REST API' },
  { key: 'grpc', note: 'RPC' },
  { key: 'loguru', note: '日志' },
  { key: 'structlog', note: '结构日志' },
  { key: 'cryptography', note: '加解密' },
  { key: 'pyjwt', note: 'JWT库' },
  { key: 'passlib', note: '密码哈希' },
  { key: 'bcrypt', note: '密码哈希' },
  { key: 'cachetools', note: '缓存' },
  { key: 'diskcache', note: '磁盘缓存' },
  { key: 'aiocache', note: '异步缓存' },
  { key: 'cacheout', note: '内存缓存' },
  { key: 'pymemcache', note: 'Memcached' },
  { key: 'redis', note: 'Redis客户端' },
  { key: 'rq', note: '任务队列' },
  { key: 'scrapy', note: '爬虫' },
  { key: 'dramatiq', note: '轻量队列' },
  { key: 'pydantic', note: '数据校验' },
  { key: 'alembic', note: '数据迁移' },
  { key: 'beautifulsoup', note: 'HTML解析' },
  { key: 'lxml', note: 'HTML解析' },
  { key: 'selenium', note: '浏览器自动化' },
  { key: 'pytest', note: '单元测试' },
  { key: 'pandas', note: '数据分析' },
  { key: 'numpy', note: '数值计算' },
  { key: 'matplotlib', note: '数据可视' },
  { key: 'seaborn', note: '统计绘图' },
  { key: 'pytorch', note: '深度学习' },
  { key: 'tensorflow', note: '机器学习' },
  { key: 'transformers', note: 'NLP模型' },
  { key: 'pillow', note: '图像处理' },
  { key: 'opencv', note: '计算机视觉' },
  { key: 'jinja2', note: '模板引擎' },
  { key: 'psycopg2', note: 'Postgres驱动' },
  { key: 'pymongo', note: 'Mongo客户端' },
  { key: 'paramiko', note: 'SSH工具' },
  { key: 'fabric', note: '部署自动化' },
  { key: 'schedule', note: '定时任务' },
  { key: 'pyinstaller', note: '可执行打包' },
  { key: 'fastcache', note: '内存缓存' },
  { key: 'faker', note: '测试造数' },
  { key: 'arrow', note: '时间处理' },
  { key: 'tenacity', note: '重试库' },
  { key: 'rich', note: '终端美化' },
  { key: 'typer', note: 'CLI' },
  { key: 'poetry', note: '依赖管理' },
  { key: 'pipenv', note: '虚拟环境' },
  { key: 'locust', note: '压力测试' },
  { key: 'streamlit', note: '数据应用' },
  { key: 'luigi', note: '工作流' },
  { key: 'prefect', note: '工作流' },
  { key: 'spring-boot', note: 'Java Web 应用' },
  { key: 'spring-web', note: 'Java Web' },
  { key: 'spring-cloud', note: '微服务' },
  { key: 'quarkus', note: '云原生 Java' },
  { key: 'micronaut', note: '云原生 Java' },
  { key: 'vertx', note: '响应式 Java' },
  { key: 'play', note: '全栈 Web' },
  { key: 'dropwizard', note: 'REST API' },
  { key: 'dubbo', note: 'RPC' },
  { key: 'spring-mvc', note: 'Web' },
  { key: 'spring-security', note: '权限安全' },
  { key: 'shiro', note: '权限认证' },
  { key: 'netty', note: '网络编程' },
  { key: 'quartz', note: '定时任务' },
  { key: 'xxl-job', note: '分布式任务' },
  { key: 'elasticsearch', note: '搜索引擎' },
  { key: 'junit5', note: '单元测试' },
  { key: 'mockito', note: 'Mock 测试' },
  { key: 'assertj', note: '断言' },
  { key: 'springdoc', note: '接口文档' },
  { key: 'mapstruct', note: '对象映射' },
  { key: 'lombok', note: '代码简化' },
  { key: 'hutool', note: '工具包' },
  { key: 'guava', note: '工具包' },
  { key: 'jackson', note: 'JSON序列' },
  { key: 'fastjson2', note: '高性能JSON' },
  { key: 'easyexcel', note: 'Excel处理' },
  { key: 'minio-sdk', note: '对象存储' },
  { key: 'sentinel', note: '限流熔断' },
  { key: 'seata', note: '分布式事务' },
  { key: 'canal', note: 'Binlog订阅' },
  { key: 'hikari', note: '连接池' },
  { key: 'skywalking', note: '链路追踪' },
  { key: 'zipkin', note: '链路追踪' },
  { key: 'easycaptcha', note: '验证码' },
  { key: 'sa-token', note: '轻量权限' },
  { key: 'jasypt', note: '配置加密' },
  { key: 'flowable', note: '工作流引擎' },
  { key: 'activiti', note: '工作流引擎' },
  { key: 'cglib', note: '动态代理' },
  { key: 'javassist', note: '字节码' },
  { key: 'vavr', note: '函数式' },
  { key: 'resilience4j', note: '熔断限流' },
  { key: 'openfeign', note: '声明式HTTP' },
  { key: 'loadbalancer', note: '负载均衡' },
  { key: 'easyretry', note: '重试' },
  { key: 'spring-data-jpa', note: '数据访问' },
  { key: 'okhttp', note: 'HTTP客户端' },
  { key: 'httpclient', note: 'HTTP客户端' },
  { key: 'retrofit', note: 'HTTP客户端' },
  { key: 'webclient', note: 'HTTP客户端' },
  { key: 'jakarta-mail', note: '邮件发送' },
  { key: 'spring-mail', note: '邮件发送' },
  { key: 'commons-io', note: '文件工具' },
  { key: 'commons-fileupload', note: '文件上传' },
  { key: 'jooq', note: '类型ORM' },
  { key: 'log4j', note: '日志' },
  { key: 'log4j2', note: '日志' },
  { key: 'logback', note: '日志' },
  { key: 'slf4j', note: '日志门面' },
  { key: 'bouncycastle', note: '加解密' },
  { key: 'jjwt', note: 'JWT库' },
  { key: 'ehcache', note: '缓存' },
  { key: 'caffeine', note: '缓存' },
  { key: 'redisson', note: 'Redis客户端' },
  { key: 'mybatis', note: 'ORM' },
  { key: 'mybatis-plus', note: 'ORM 增强' },
  { key: 'hibernate', note: 'JPA' },
  { key: 'gin', note: 'Go Web' },
  { key: 'echo', note: 'Go Web' },
  { key: 'fiber', note: '高性能 Go Web' },
  { key: 'beego', note: 'Go 全栈 Web' },
  { key: 'chi', note: 'Go 路由' },
  { key: 'iris', note: 'Go Web' },
  { key: 'revel', note: 'Go 全栈 Web' },
  { key: 'gorm', note: 'ORM' },
  { key: 'sqlx', note: 'SQL工具' },
  { key: 'kratos', note: '微服务' },
  { key: 'logrus', note: '日志' },
  { key: 'zap', note: '日志' },
  { key: 'resty', note: 'HTTP客户端' },
  { key: 'fasthttp', note: '高性能HTTP' },
  { key: 'gomail', note: '邮件发送' },
  { key: 'gosimplemail', note: '邮件发送' },
  { key: 'afero', note: '文件系统' },
  { key: 'aws-sdk-go', note: '对象存储' },
  { key: 'minio-go', note: '对象存储' },
  { key: 'ent', note: 'ORM' },
  { key: 'bun', note: 'ORM' },
  { key: 'sqlc', note: 'SQL生成' },
  { key: 'zerolog', note: '日志' },
  { key: 'jwt-go', note: 'JWT库' },
  { key: 'ristretto', note: '缓存' },
  { key: 'bigcache', note: '缓存' },
  { key: 'go-redis', note: 'Redis客户端' },
  { key: 'nats', note: '消息队列' },
  { key: 'nsq', note: '消息队列' },
  { key: 'amqp', note: '消息队列' },
  { key: 'laravel', note: 'PHP 全栈 Web' },
  { key: 'symfony', note: 'PHP 企业 Web' },
  { key: 'thinkphp', note: 'PHP Web' },
  { key: 'yii', note: '高性能 PHP Web' },
  { key: 'slim', note: 'PHP 微 Web' },
  { key: 'lumen', note: 'PHP 微服务' },
  { key: 'codeigniter', note: 'PHP 轻量 Web' },
  { key: 'doctrine', note: 'ORM' },
  { key: 'eloquent', note: 'ORM' },
  { key: 'blade', note: '模板引擎' },
  { key: 'twig', note: '模板引擎' },
  { key: 'phpmailer', note: '邮件发送' },
  { key: 'swiftmailer', note: '邮件发送' },
  { key: 'symfony/mailer', note: '邮件发送' },
  { key: 'guzzle', note: 'HTTP客户端' },
  { key: 'symfony/http-client', note: 'HTTP客户端' },
  { key: 'flysystem', note: '文件系统' },
  { key: 'symfony/filesystem', note: '文件系统' },
  { key: 'predis', note: 'Redis客户端' },
  { key: 'symfony/cache', note: '缓存' },
  { key: 'php-amqplib', note: '消息队列' },
  { key: 'php-jwt', note: 'JWT库' },
  { key: 'phpseclib', note: '加解密' },
  { key: 'propel', note: 'ORM' },
  { key: 'rails', note: 'Ruby 全栈 Web' },
  { key: 'rocket', note: 'Rust Web' },
  { key: 'actix', note: 'Rust Web' },
  { key: 'warp', note: '异步 Web' },
  { key: 'axum', note: '异步 Web' },
  { key: 'tide', note: '异步 Web' },
  { key: 'reqwest', note: 'HTTP客户端' },
  { key: 'hyper', note: 'HTTP客户端' },
  { key: 'lettre', note: '邮件发送' },
  { key: 'sea-orm', note: 'ORM' },
  { key: 'sqlx', note: 'SQL' },
  { key: 'redis', note: 'Redis客户端' },
  { key: 'moka', note: '缓存' },
  { key: 'tracing', note: '链路日志' },
  { key: 'log', note: '日志' },
  { key: 'env_logger', note: '日志' },
  { key: 'ring', note: '加解密' },
  { key: 'jsonwebtoken', note: 'JWT库' },
  { key: 'argon2', note: '密码哈希' },
  { key: 'object_store', note: '对象存储' },
  { key: 'async-std', note: '异步文件' },
  { key: 'diesel', note: 'ORM' },
  { key: 'serde', note: '序列化' },
  { key: 'aspnetcore', note: '.NET Web' },
  { key: 'nancy', note: '轻量 .NET Web' },
  { key: 'entity-framework', note: '.NET ORM' },
  { key: 'dapper', note: '.NET微ORM' },
  { key: 'serilog', note: '.NET日志' },
  { key: 'nlog', note: '.NET日志' },
  { key: 'mailkit', note: '邮件发送' },
  { key: 'fluentemail', note: '邮件发送' },
  { key: 'restsharp', note: 'HTTP客户端' },
  { key: 'refit', note: 'HTTP客户端' },
  { key: 'stackexchange.redis', note: 'Redis客户端' },
  { key: 'memorycache', note: '内存缓存' },
  { key: 'masstransit', note: '消息队列' },
  { key: 'rabbitmq.client', note: '消息队列' },
  { key: 'awssdk.s3', note: '对象存储' },
  { key: 'azure-storage-blob', note: '对象存储' },
  { key: 'minio', note: '对象存储' },
  { key: 'mongo.driver', note: 'Mongo驱动' },
  { key: 'log4net', note: '.NET 日志' },
  { key: 'bouncycastle', note: '加解密' },
  { key: 'jwtbearer', note: 'JWT认证' },
  { key: 'axios', note: 'HTTP 客户端' },
  { key: 'node-fetch', note: 'HTTP 客户端' },
  { key: 'cross-fetch', note: 'HTTP 客户端' },
  { key: 'body-parser', note: '请求体解析' },
  { key: 'consul', note: '服务发现配置' },
  { key: 'cors', note: '跨域中间件' },
  { key: 'crypto', note: '加解密哈希' },
  { key: 'emailjs', note: '邮件发送' },
  { key: 'excel-export', note: 'Excel 导出' },
  { key: 'excel-report', note: 'Excel 报表' },
  { key: 'fastdfs-client', note: 'FastDFS 客户端' },
  { key: 'file-stream-rotator', note: '日志切割' },
  { key: 'forever', note: '进程守护' },
  { key: 'http', note: 'HTTP 库' },
  { key: 'moment', note: '时间日期' },
  { key: 'react', note: 'UI 库' },
  { key: 'vue', note: 'UI 库' },
  { key: 'angular', note: '企业 UI' },
  { key: 'svelte', note: 'UI 库' },
  { key: 'solid', note: '高性能 UI' },
  { key: 'preact', note: '轻量 UI' },
  { key: 'next', note: 'SSR/静态站' },
  { key: 'nuxt', note: 'SSR/静态站' },
  { key: 'gatsby', note: '静态站点' },
  { key: 'astro', note: '静态站点' },
  { key: 'remix', note: '全栈路由' },
  { key: 'sveltekit', note: '全栈 Web' },
  { key: 'vite', note: '前端构建' },
  { key: 'webpack', note: '打包工具' },
  { key: 'rollup', note: '库打包' },
  { key: 'esbuild', note: '极速打包' },
  { key: 'babel', note: '转译工具' },
  { key: 'parcel', note: '零配置打包' },
  { key: 'snowpack', note: '按需构建' },
  { key: 'typescript', note: '类型支持' },
  { key: 'ts-node', note: 'TS 运行' },
  { key: 'ts-node-dev', note: 'TS 热重载' },
  { key: 'react-router', note: 'React 路由' },
  { key: 'vue-router', note: 'Vue 路由' },
  { key: 'tanstack-router', note: '类型安全路由' },
  { key: 'wouter', note: '轻量路由' },
  { key: 'redux', note: '状态管理' },
  { key: 'zustand', note: '状态管理' },
  { key: 'jotai', note: '原子化状态' },
  { key: 'recoil', note: '原子化状态' },
  { key: 'pinia', note: 'Vue3 状态' },
  { key: 'vuex', note: 'Vue2 状态' },
  { key: 'swr', note: '数据获取' },
  { key: 'react-query', note: '数据获取' },
  { key: 'apollo', note: 'GraphQL 客户端' },
  { key: 'urql', note: 'GraphQL 客户端' },
  { key: 'tailwind', note: '样式' },
  { key: 'tailwindcss', note: '样式' },
  { key: 'sass', note: '预处理器' },
  { key: 'less', note: '预处理器' },
  { key: 'styled-components', note: 'CSS-in-JS' },
  { key: 'emotion', note: 'CSS-in-JS' },
  { key: 'postcss', note: '样式管线' },
  { key: 'bootstrap', note: 'UI 样式' },
  { key: 'antd', note: 'UI 组件库' },
  { key: 'mui', note: 'UI 组件库' },
  { key: 'element-plus', note: 'Vue3 组件' },
  { key: 'chakra', note: 'UI 组件库' },
  { key: 'shadcn', note: 'UI 组件库' },
  { key: 'headlessui', note: '无样式组件' },
  { key: 'radix', note: '无样式组件' },
  { key: 'mantine', note: 'UI 组件库' },
  { key: 'playwright', note: 'E2E/自动化' },
  { key: 'cypress', note: 'E2E 测试' },
  { key: 'jest', note: '单元测试' },
  { key: 'vitest', note: '单元测试' },
  { key: 'mocha', note: '单元测试' },
  { key: 'testing-library', note: '组件测试' },
  { key: 'eslint', note: '代码检查' },
  { key: 'prettier', note: '代码格式化' },
  { key: 'husky', note: 'Git 钩子' },
  { key: 'lint-staged', note: '提交前检查' },
  { key: 'prisma', note: 'ORM/数据库' },
  { key: 'typeorm', note: 'ORM/数据库' },
  { key: 'mongoose', note: 'MongoDB ODM' },
  { key: 'sequelize', note: 'ORM/数据库' },
  { key: 'pg', note: 'PostgreSQL 驱动' },
  { key: 'mysql', note: 'MySQL 驱动' },
  { key: 'redis', note: 'Redis 客户端' },
  { key: 'winston', note: '日志' },
  { key: 'pino', note: '日志' },
  { key: 'bunyan', note: '日志' },
  { key: 'dotenv', note: '环境变量' },
  { key: 'config', note: '配置管理' },
  { key: 'pm2', note: '进程守护' },
  { key: 'nodemon', note: '开发重启' },
  { key: 'bull', note: '队列/任务' },
  { key: 'agenda', note: '队列/任务' },
  { key: 'socket.io', note: '实时通信' },
  { key: 'ws', note: 'WebSocket' },
  { key: 'jsonwebtoken', note: 'JWT 认证' },
  { key: 'passport', note: '认证' },
  { key: 'swagger', note: '接口文档' },
  { key: 'openapi', note: '接口文档' }
  ,{ key: 'nestjs', note: '企业级 Web' }
  ,{ key: 'nextjs', note: 'React SSR' }
  ,{ key: 'nuxtjs', note: 'Vue SSR' }
  ,{ key: 'sequelize', note: 'ORM' }
  ,{ key: 'mikro-orm', note: '高性能ORM' }
  ,{ key: 'objection', note: 'SQL ORM' }
  ,{ key: 'chai', note: '断言库' }
  ,{ key: 'supertest', note: 'API测试' }
  ,{ key: 'nextauth', note: '全栈认证' }
  ,{ key: 'undici', note: 'HTTP客户端' }
  ,{ key: 'multer', note: '文件上传' }
  ,{ key: 'sharp', note: '图片处理' }
  ,{ key: 'nodemailer', note: '邮件发送' }
  ,{ key: 'joi', note: '数据校验' }
  ,{ key: 'zod', note: 'TS校验' }
  ,{ key: 'ejs', note: '模板引擎' }
  ,{ key: 'handlebars', note: '模板引擎' }
  ,{ key: 'ioredis', note: 'Redis客户端' }
  ,{ key: 'amqplib', note: 'RabbitMQ客户端' }
  ,{ key: 'kafkajs', note: 'Kafka客户端' }
  ,{ key: 'dayjs', note: '轻量时间' }
  ,{ key: 'fakerjs', note: '测试造数' }
  ,{ key: 'helmet', note: '安全防护' }
  ,{ key: 'compression', note: '压缩中间件' }
  ,{ key: 'morgan', note: '请求日志' }
  ,{ key: 'nanoid', note: '唯一ID' }
  ,{ key: 'go-zero', note: '微服务' }
  ,{ key: 'kitex', note: 'RPC' }
  ,{ key: 'hertz', note: 'HTTP' }
  ,{ key: 'xorm', note: '轻量ORM' }
  ,{ key: 'sqlboiler', note: '代码生成' }
  ,{ key: 'grpc-gateway', note: 'gRPC转HTTP' }
  ,{ key: 'viper', note: '配置管理' }
  ,{ key: 'cobra', note: 'CLI' }
  ,{ key: 'testify', note: '测试工具' }
  ,{ key: 'goconvey', note: '可视化测试' }
  ,{ key: 'goredis', note: 'Redis客户端' }
  ,{ key: 'redigo', note: 'Redis客户端' }
  ,{ key: 'sarama', note: 'Kafka客户端' }
  ,{ key: 'ffmpeg-go', note: '音视频' }
  ,{ key: 'image', note: '图片处理' }
  ,{ key: 'cron', note: '定时任务' }
  ,{ key: 'asynq', note: '异步任务' }
  ,{ key: 'machinery', note: '任务队列' }
  ,{ key: 'ginkgo', note: '测试' }
  ,{ key: 'gomega', note: '断言库' }
  ,{ key: 'dig', note: '依赖注入' }
  ,{ key: 'wire', note: '依赖注入' }
  ,{ key: 'hystrix-go', note: '熔断限流' }
  ,{ key: 'sentinel-go', note: '流量治理' }
  ,{ key: 'opentelemetry', note: '链路追踪' }
  ,{ key: 'prometheus', note: '监控指标' }
  ,{ key: 'gops', note: '进程诊断' }
  ,{ key: 'pprof', note: '性能分析' }
  ,{ key: 'goldmark', note: 'Markdown解析' }
  ,{ key: 'swaggo', note: 'Swagger文档' }
  ,{ key: 'validator', note: '数据校验' }
  ,{ key: 'uuid', note: '唯一ID' }
  ,{ key: 'bcrypt-go', note: '密码加密' }
  ,{ key: 'phalcon', note: '高性能 Web' }
  ,{ key: 'cakephp', note: '全栈 Web' }
  ,{ key: 'laminas', note: '企业 Web' }
  ,{ key: 'phpunit', note: '单元测试' }
  ,{ key: 'codeception', note: '全栈测试' }
  ,{ key: 'intervention-image', note: '图片处理' }
  ,{ key: 'phpspreadsheet', note: 'Excel处理' }
  ,{ key: 'laravel-passport', note: 'OAuth2' }
  ,{ key: 'laravel-sanctum', note: '轻量认证' }
  ,{ key: 'swoole', note: '协程' }
  ,{ key: 'openswoole', note: '协程' }
  ,{ key: 'workerman', note: '长连接服务' }
  ,{ key: 'laravel-octane', note: '协程加速' }
  ,{ key: 'inertia', note: '同构' }
  ,{ key: 'livewire', note: '无JS交互' }
  ,{ key: 'laravel-horizon', note: '队列管理' }
  ,{ key: 'carbon', note: '时间处理' }
  ,{ key: 'hashids', note: 'ID加密' }
  ,{ key: 'php-enums', note: '枚举扩展' }
  ,{ key: 'tinker', note: '命令行交互' }
  ,{ key: 'telescope', note: '调试工具' }
  ,{ key: 'socialite', note: '第三方登录' }
  ,{ key: 'laravel-scout', note: '全文搜索' }
  ,{ key: 'dusk', note: '浏览器测试' }
  ,{ key: 'breeze', note: '认证脚手架' }
  ,{ key: 'jetstream', note: '增强脚手架' }
  ,{ key: 'filament', note: '后台管理' }
  ,{ key: 'nova', note: '官方后台' }
  ,{ key: 'easywechat', note: '微信开发' }
  ,{ key: 'overtrue', note: '工具包' }
  ,{ key: 'php-di', note: 'IOC容器' }
  ,{ key: 'php-cs-fixer', note: '代码规范' }
  ,{ key: 'phpstan', note: '静态分析' }
  ,{ key: 'ramsey/uuid', note: '唯一ID' }
  ,{ key: 'respect/validation', note: '数据验证' }
  ,{ key: 'medialibrary', note: '文件管理' }
  ,{ key: 'maatwebsite/excel', note: 'Excel导入导出' }
  ,{ key: 'core-js', note: 'JS补丁库' }
  ,{ key: 'electron', note: '桌面应用' }
  ,{ key: 'electron-rebuild', note: '原生重编译' }
  ,{ key: 'electron-devtools-installer', note: '开发者工具' }
  ,{ key: 'lndb', note: '本地数据库' }
  ,{ key: 'node-cmd', note: '命令执行' }
  ,{ key: 'node-notifier', note: '系统通知' }
  ,{ key: 'portfinder', note: '端口探测' }
  ,{ key: 'robotjs', note: '桌面自动化' }
  ,{ key: 'log4js', note: '日志' }
  ,{ key: '@vue/cli-plugin-babel', note: 'Vue Babel' }
  ,{ key: '@vue/cli-plugin-eslint', note: 'Vue ESLint插件' }
  ,{ key: '@vue/cli-service', note: 'Vue 服务' }
  ,{ key: 'vue-cli-plugin-electron-builder', note: 'Electron构建' }
  ,{ key: 'vue-template-compiler', note: '模板编译' }
  ,{ key: 'eslint-plugin-vue', note: 'Vue ESLint' }
  ,{ key: 'blazor', note: 'UI' }
  ,{ key: 'signalr', note: '实时通信' }
  ,{ key: 'automapper', note: '对象映射' }
  ,{ key: 'mediatr', note: '中介者模式' }
  ,{ key: 'fluentvalidation', note: '数据验证' }
  ,{ key: 'xunit', note: '单元测试' }
  ,{ key: 'nunit', note: '测试' }
  ,{ key: 'moq', note: 'Mock' }
  ,{ key: 'nsubstitute', note: 'Mock' }
  ,{ key: 'hangfire', note: '后台任务' }
  ,{ key: 'quartz.net', note: '定时任务' }
  ,{ key: 'aspnet-identity', note: '身份认证' }
  ,{ key: 'identityserver', note: 'OAuth授权' }
  ,{ key: 'ocelot', note: 'API网关' }
  ,{ key: 'steeltoe', note: '微服务套件' }
  ,{ key: 'sixlabors.imagesharp', note: '图片处理' }
  ,{ key: 'epplus', note: 'Excel处理' }
  ,{ key: 'masstransit', note: '消息总线' }
  ,{ key: 'rebus', note: '消息总线' }
  ,{ key: 'easycaching', note: '多级缓存' }
  ,{ key: 'npgsql', note: 'Postgres驱动' }
  ,{ key: 'pomelo.mysql', note: 'MySQL驱动' }
  ,{ key: 'miniprofiler', note: '性能分析' }
  ,{ key: 'swashbuckle', note: 'Swagger文档' }
  ,{ key: 'faker.net', note: '测试造数' }
  ,{ key: 'humanizer', note: '字符串美化' }
  ,{ key: 'cronos', note: 'Cron解析' }
  ,{ key: 'polly', note: '熔断重试' }
  ,{ key: 'benchmarkdotnet', note: '性能基准' }
  ,{ key: 'autofac', note: 'IOC容器' }
  ,{ key: 'lamar', note: 'IOC容器' }
  ,{ key: 'litedb', note: '嵌入式库' }
  ,{ key: 'elasticsearch.net', note: 'ES客户端' }
  ,{ key: 'nest-client', note: 'ES高级客户端' }
  ,{ key: 'dotnetty', note: '网络编程' }
  ,{ key: 'grpc.net', note: 'gRPC' }
  ,{ key: 'graphql.net', note: 'GraphQL 服务' }
  ,{ key: 'hotchocolate', note: 'GraphQL' }
  ,{ key: 'fluentassertions', note: '断言库' }
  ,{ key: 'sharpziplib', note: '压缩解压' }
  ,{ key: 'microsoft.ioc', note: 'IOC容器' }
  ,{ key: 'netescapades.enumgenerators', note: '枚举增强' }
  ,{ key: 'autoprefixer', note: 'CSS前缀' }
  ,{ key: 'chalk', note: '终端着色' }
  ,{ key: 'connect-history-api-fallback', note: '路由兜底' }
  ,{ key: 'copy-webpack-plugin', note: '文件拷贝' }
  ,{ key: 'css-loader', note: 'CSS加载' }
  ,{ key: 'babel-plugin-transform-runtime', note: '运行时提取' }
  ,{ key: 'eslint-plugin-html', note: 'HTML ESLint' }
  ,{ key: 'eslint-plugin-promise', note: 'Promise规范' }
];

function findUsage(name) {
  const lower = name.toLowerCase();
  const hit = DEP_USAGE.find((item) => lower.includes(item.key));
  return hit ? hit.note : '用途待查';
}

function renderDepsGrid(deps, title) {
  const entries = deps ? Object.entries(deps) : [];
  if (entries.length === 0) return `<p class="muted">${title}：暂无</p>`;
  const cards = entries.slice(0, 18)
    .map(([name, version]) => {
      const note = findUsage(name);
      const showVersion = version && !version.includes('${');
      return `<div class="dep-card"><div class="dep-line"><span class="dep-name">${name}</span>${showVersion ? `<span class="muted">${version}</span>` : ''}</div><div class="dep-note">${note}</div></div>`;
    })
    .join('');
  return `
    <div class="dep-block">
      <h3>${title}</h3>
      <div class="dep-grid">${cards}</div>
    </div>
  `;
}

function renderDepsSection(packageInfo, packageManager) {
  const hasPkg = !!packageInfo;
  const hasDeps = hasPkg && packageInfo.dependencies && Object.keys(packageInfo.dependencies).length > 0;
  const pmLabel = packageInfo && packageInfo.label ? packageInfo.label : (packageManager || '未检测到包管理文件');

  if (!hasDeps) {
    return `<div class="section"><h2>🛠️ 依赖</h2><p class="muted">${pmLabel}，依赖信息暂无</p></div>`;
  }

  const deps = renderDepsGrid(packageInfo ? packageInfo.dependencies : null, 'dependencies');
  return `
    <div class="section">
      <h2>🛠️ 依赖</h2>
      <p class="muted" style="margin-bottom:8px;">来源：${pmLabel}</p>
      ${deps}
    </div>
  `;
}

function renderLanguages(languages) {
  if (!languages || languages.length === 0) return '<p class="muted">未识别语言</p>';
  return languages
    .sort((a, b) => b.count - a.count)
    .map((lang) => `<span class="tag subtle">${lang.name} · ${lang.count}</span>`)
    .join('');
}

function renderDirs(dirs) {
  if (!dirs || dirs.length === 0) return '<p class="muted">未检测到目录结构</p>';
  return dirs
    .sort((a, b) => b.count - a.count)
    .slice(0, 8)
    .map((dir) => `<span class="tech-tag">${dir.name} (${dir.count})</span>`)
    .join('');
}

function renderReadme(readmeHtml, fallback, githubInfo, gitUrl) {
  if (readmeHtml) {
    return `<div class="section"><h2>📖 项目介绍</h2><div class="readme">${readmeHtml}</div></div>`;
  }
  return `<div class="section"><h2>📖 项目介绍</h2><p class="muted">暂无介绍，请点击上方按钮编辑添加...</p></div>`;
}

function renderThemeOptions(current) {
  return Object.keys(THEMES)
    .map((key) => {
      const checked = key === current ? 'checked' : '';
      return `<label class="theme-option"><input type="radio" name="theme" value="${key}" ${checked}/> ${key}</label>`;
    })
    .join('');
}

function renderHtml(data, theme) {
  const themeOptions = renderThemeOptions(theme.name);
  const languages = renderLanguages(data.stats.languages || []);
  const dirs = renderDirs(data.stats.topDirs || []);
  const fallback = data.description || `基于代码结构自动生成：共 ${data.stats.totalFiles} 个文件，主要语言 ${data.stats.languages.map((l) => l.name).slice(0, 3).join('、') || '未知'}`;

  const themeJson = JSON.stringify(THEMES);

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${data.projectName} - 介绍</title>
  <style>
    :root {
      --bg: ${theme.background};
      --header: ${theme.header};
      --accent: ${theme.accent};
      --text: ${theme.textPrimary};
      --text-2: ${theme.textSecondary};
      --card: ${theme.card};
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); padding: 16px 8px; color: var(--text); font-size: 22px; line-height: 1.7; }
    .container { width: 100%; max-width: 100%; margin: 0 auto; background: var(--card); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.18); backdrop-filter: blur(10px); }
    .header { background: var(--header); color: white; padding: 20px 18px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
    .header h1 { margin: 0; font-size: 2.8rem; }
    .section { padding: 18px; border-bottom: 1px solid rgba(0,0,0,0.05); }
    .section:last-child { border-bottom: none; }
    h2 { margin: 0 0 14px 0; font-size: 26px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
    h3 { margin: 0 0 6px 0; font-size: 22px; font-weight: 600; }
    .tag { display: inline-block; background: var(--accent); color: white; padding: 6px 12px; border-radius: 12px; font-size: 20px; margin: 3px; }
    .tag.subtle { background: rgba(102,126,234,0.12); color: var(--text); border: 1px solid rgba(102,126,234,0.25); font-size: 20px; }
    .tech-tag { background: rgba(0,0,0,0.04); color: var(--text); padding: 6px 10px; border-radius: 8px; font-size: 20px; margin: 3px; display: inline-block; }
    .note { background: rgba(255, 247, 230, 0.9); border-left: 4px solid #ffb347; padding: 12px 14px; border-radius: 10px; color: #6b4e16; line-height: 1.6; }
    .muted { color: var(--text-2); font-size: 22px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
    .card { background: rgba(255,255,255,0.6); border-radius: 12px; padding: 18px; box-shadow: 0 6px 20px rgba(0,0,0,0.05); }
    .readme { background: rgba(0,0,0,0.02); border-radius: 12px; padding: 14px; line-height: 1.7; }
    .readme h1, .readme h2, .readme h3, .readme h4 { margin-top: 14px; margin-bottom: 10px; }
    .readme p { margin: 12px 0; color: var(--text-2); }
    .readme pre { background: #0f172a; color: #e2e8f0; padding: 16px; border-radius: 10px; overflow: auto; font-size: 26px; line-height: 1.9; }
    .readme code { background: rgba(0,0,0,0.08); padding: 2px 8px; border-radius: 6px; font-size: 24px; }
    .dep-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }
    .dep-card { background: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.05); border-radius: 10px; padding: 10px; }
    .dep-line { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; font-weight: 600; }
    .dep-note { color: var(--text-2); font-size: 0.85rem; margin-top: 4px; }
    .dep-block { margin-bottom: 14px; }
    .footer { background: rgba(0,0,0,0.02); padding: 16px; text-align: center; font-size: 18px; color: var(--text-2); }
    .footer-spacer { height: 500px; }
    .pill { display: inline-flex; align-items: center; gap: 6px; background: rgba(0,0,0,0.05); padding: 6px 10px; border-radius: 999px; font-size: 0.85rem; color: var(--text-2); }
    .toolbar { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
    .theme-option { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.15); padding: 6px 10px; border-radius: 12px; color: white; border: 1px solid rgba(255,255,255,0.25); }
    .btn { border: none; padding: 8px 12px; border-radius: 10px; background: white; color: #1f2937; cursor: pointer; font-weight: 600; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .btn.export { background: #2563eb; color: white; }
    body.exporting .toolbar { display: none; }
    .export-mode .toolbar { display: none !important; }
    body.export-mode { padding: 0; background: white; }
    .export-mode .container { border-radius: 0; box-shadow: none; margin: 0; width: 100%; max-width: 100%; }
    .modal { position: fixed; inset: 0; display: none; align-items: center; justify-content: center; background: rgba(0,0,0,0.4); z-index: 9999; }
    .modal.open { display: flex; }
    .modal-content { background: #fff; padding: 18px; border-radius: 12px; max-width: 520px; width: calc(100% - 40px); box-shadow: 0 16px 50px rgba(0,0,0,0.15); color: #111827; }
    .modal-content h3 { margin: 0 0 10px 0; font-size: 1rem; }
    .path-box { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; word-break: break-all; font-family: monospace; font-size: 0.82rem; color: #111827; line-height: 1.4; }
    .cmd-line { color: var(--accent); font-weight: 600; }
    .modal-actions { margin-top: 12px; display: flex; gap: 10px; justify-content: flex-end; }
    .spinner { width: 18px; height: 18px; border: 3px solid #e5e7eb; border-top-color: #2563eb; border-radius: 50%; animation: spin 1s linear infinite; display: inline-block; margin-right: 6px; }
    @keyframes spin { to { transform: rotate(360deg); } }
    @media (max-width: 640px) {
      body { font-size: 22px; padding: 10px 6px; }
      .header { flex-direction: column; align-items: flex-start; }
    }
  </style>
</head>
<body>
  <div class="container" contenteditable="true">
    <div class="header">
      <div>
        <h1>${data.projectName}</h1>
      </div>
      <div class="toolbar">
        <span class="pill">主题</span>
        ${themeOptions}
        <button class="btn" id="save-btn" onclick="saveHtml()">保存修改并导出图片</button>
      </div>
    </div>

    <div class="section">
      <h2>📊 项目概览</h2>
      <div class="grid">
        <div class="card"><h3>文件数</h3><p class="muted">${data.stats.totalFiles}</p></div>
        <div class="card"><h3>主要语言</h3>${languages}</div>
        <div class="card"><h3>目录</h3>${dirs}</div>
      </div>
    </div>

    ${renderReadme(data.readmeHtml, fallback, data.githubInfo, data.gitUrl)}

    ${renderDepsSection(data.packageInfo, data.packageManager)}

    <div class="footer-spacer" aria-hidden="true"></div>
  </div>

  <div class="footer">
    <div>生成时间：${new Date(data.generatedAt).toLocaleString()}</div>
  </div>

  <script>
    const themes = ${themeJson};
    const imagePath = ${JSON.stringify(data.imagePath || '')};
    const htmlPath = ${JSON.stringify(data.htmlPath || '')};
    const projectPath = ${JSON.stringify(data.projectPath || '')};
    const gitUrl = ${JSON.stringify(data.gitUrl || '')};
    const cliPath = ${JSON.stringify(data.cliPath || '')};
    const themeName = ${JSON.stringify(data.themeName || 'aurora')};
    const projectName = ${JSON.stringify(data.projectName || 'introshow')};
    function applyTheme(name) {
      const t = themes[name] || themes['aurora'];
      document.documentElement.style.setProperty('--bg', t.background);
      document.documentElement.style.setProperty('--header', t.header);
      document.documentElement.style.setProperty('--accent', t.accent);
      document.documentElement.style.setProperty('--text', t.textPrimary);
      document.documentElement.style.setProperty('--text-2', t.textSecondary);
      document.documentElement.style.setProperty('--card', t.card);
      localStorage.setItem('introshow-theme', name);
    }
    const stored = localStorage.getItem('introshow-theme');
    if (stored && themes[stored]) { applyTheme(stored); }
    document.querySelectorAll('input[name="theme"]').forEach((input) => {
      input.addEventListener('change', (e) => { applyTheme(e.target.value); });
    });

    let modalTitle = null;
    let pathBox = null;
    const editedPlaceholder = '[已下载HTML绝对路径]';
    let latestSavedHtml = '';
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = '<div class="modal-content">' +
      '<h3 id="modal-title">导出图片</h3>' +
      '<div class="path-box" id="img-path-box"></div>' +
      '<div class="modal-actions">' +
        '<button class="btn" id="close-modal">关闭</button>' +
        '<button class="btn export" id="copy-path">复制命令</button>' +
      '</div>' +
    '</div>';
    document.body.appendChild(modal);
    modalTitle = document.getElementById('modal-title');
    pathBox = document.getElementById('img-path-box');
    document.getElementById('close-modal').onclick = () => modal.classList.remove('open');
    let cmdForCopy = '';
    document.getElementById('copy-path').onclick = () => {
      const txt = cmdForCopy || '';
      if (!txt) return;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(txt).then(() => { alert('已复制指令'); });
      } else {
        const ta = document.createElement('textarea');
        ta.value = txt; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
        alert('已复制指令');
      }
    };

    function showImagePath() {
      const box = pathBox || document.getElementById('img-path-box');
      if (!imagePath) {
        box.textContent = '长图已生成，请在 output 目录查看对应 .png 文件。';
      } else {
        box.textContent = imagePath;
      }
      modal.classList.add('open');
    }

    function wrapPath(p) {
      if (!p) return '';
      return p.includes(' ') ? '"' + p + '"' : p;
    }

    function saveHtml() {
      const html = '<!DOCTYPE html>' + document.documentElement.outerHTML;
      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const editedName = projectName + '-edited-' + Date.now() + '.html';
      a.download = editedName;
      a.click();
      URL.revokeObjectURL(url);
      latestSavedHtml = editedName;
      modalTitle.textContent = '已保存';
      const imgForCmd = imagePath || '[PNG输出路径]';
      const htmlHint = '[下载目录]/' + editedName;
      const cmd = 'node ' + wrapPath(cliPath) + ' --html ' + wrapPath(htmlHint) + ' --image-out ' + wrapPath(imgForCmd);
      cmdForCopy = cmd;
      pathBox.innerHTML = '<small><strong style="color:#dc2626;">将 ' + htmlHint + ' 换成该文件的绝对路径再执行。</strong></small>' +
        '<br>如需更新 PNG，请运行：<br><span class="cmd-line">' + cmd + '</span>';
      modal.classList.add('open');
    }

  </script>
</body>
</html>`;
}

module.exports = {
  renderHtml
};
