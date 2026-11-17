# Maven POM 模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
                             http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.jenkins-ci.plugins</groupId>
        <artifactId>plugin</artifactId>
        <version><!-- 版本根据Jenkins版本确定 --></version>
    </parent>
    
    <groupId><!-- 用户提供 --></groupId>
    <artifactId><!-- 用户提供 --></artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>hpi</packaging>
    <name><!-- 用户提供 --></name>
    
    <properties>
        <jenkins.version><!-- 用户提供 --></jenkins.version>
        <java.level><!-- 用户提供 --></java.level>
    </properties>

    <repositories>
        <repository>
            <id>repo.jenkins-ci.org</id>
            <url>https://repo.jenkins-ci.org/public/</url>
        </repository>
    </repositories>

    <pluginRepositories>
        <pluginRepository>
            <id>repo.jenkins-ci.org</id>
            <url>https://repo.jenkins-ci.org/public/</url>
        </pluginRepository>
    </pluginRepositories>
    
    <dependencies>
        <dependency>
            <groupId>org.jenkins-ci.main</groupId>
            <artifactId>jenkins-core</artifactId>
            <version>${jenkins.version}</version>
            <scope>provided</scope>
        </dependency>
        <!-- 根据插件类型添加其他依赖 -->
    </dependencies>
</project>
```
