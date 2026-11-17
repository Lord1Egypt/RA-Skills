# 项目目录结构

```
plugin-name/
├── pom.xml
├── README.md
├── .gitignore
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/plugin/   # 按包名生成
│   │   │       ├── YourPlugin.java          # 主扩展类
│   │   │       ├── YourPluginDescriptor.java # Descriptor
│   │   │       └── config/                  # 配置类（如需要）
│   │   ├── resources/
│   │   │   ├── com/example/plugin/
│   │   │   │   └── YourPlugin/             # 资源文件
│   │   │   │       ├── config.jelly        # 配置界面
│   │   │   │       └── help.html           # 帮助文档
│   │   │   └── index.jelly                 # 全局配置（如需要）
│   │   └── webapp/
│   │       └── images/
│   └── test/
│       └── java/
│           └── com/example/plugin/
│               └── YourPluginTest.java
```
