#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版一键启动脚本
支持远程数据库执行、智能服务检测、自动浏览器打开
"""

import os
import sys
import time
import json
import subprocess
import threading
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class Colors:
    """颜色输出"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class DatabaseExecutor:
    """数据库执行器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.connection = None
    
    def test_connection(self) -> Tuple[bool, str]:
        """测试数据库连接"""
        try:
            import pymysql
            conn = pymysql.connect(
                host=self.config['host'],
                port=int(self.config['port']),
                user=self.config['user'],
                password=self.config['password'],
                connect_timeout=5
            )
            conn.close()
            return True, "连接成功"
        except ImportError:
            return False, "请先安装pymysql: pip install pymysql"
        except Exception as e:
            return False, f"连接失败: {str(e)}"
    
    def execute_sql_file(self, sql_file: Path) -> Tuple[bool, List[str]]:
        """执行SQL文件"""
        if not sql_file.exists():
            return False, ["SQL文件不存在"]
        
        try:
            import pymysql
            
            conn = pymysql.connect(
                host=self.config['host'],
                port=int(self.config['port']),
                user=self.config['user'],
                password=self.config['password']
            )
            
            cursor = conn.cursor()
            errors = []
            
            # 读取SQL文件
            sql_content = sql_file.read_text(encoding='utf-8')
            
            # 分片执行（避免大文件内存问题）
            sql_statements = self._split_sql(sql_content)
            
            print(f"{Colors.CYAN}🗄️  正在执行SQL脚本...{Colors.RESET}")
            for i, statement in enumerate(sql_statements, 1):
                statement = statement.strip()
                if not statement or statement.startswith('--'):
                    continue
                
                try:
                    cursor.execute(statement)
                    conn.commit()
                    print(f"{Colors.GREEN}✅ 执行成功 ({i}/{len(sql_statements)}): {statement[:50]}...{Colors.RESET}")
                except Exception as e:
                    error_msg = f"SQL执行失败: {str(e)}\n语句: {statement[:100]}"
                    errors.append(error_msg)
                    print(f"{Colors.RED}❌ {error_msg}{Colors.RESET}")
            
            conn.close()
            return len(errors) == 0, errors
            
        except Exception as e:
            return False, [f"数据库连接失败: {str(e)}"]
    
    def _split_sql(self, sql_content: str) -> List[str]:
        """分片SQL内容"""
        # 按分号分割，但需要考虑字符串中的分号
        statements = []
        current = ""
        in_string = False
        string_char = None
        
        for char in sql_content:
            if char in ["'", '"', '`'] and (not current or current[-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
            elif char == ';' and not in_string:
                if current.strip():
                    statements.append(current.strip())
                current = ""
                continue
            
            current += char
        
        if current.strip():
            statements.append(current.strip())
        
        return statements

class ServiceMonitor:
    """服务监控器"""
    
    def __init__(self, timeout: int = 60, interval: int = 3):
        self.timeout = timeout
        self.interval = interval
        self.results = {}
    
    def check_service(self, name: str, url: str, max_attempts: int = 10) -> bool:
        """检查服务是否可用"""
        print(f"{Colors.CYAN}🔍 正在检查{name}服务: {url}{Colors.RESET}")
        
        for attempt in range(1, max_attempts + 1):
            try:
                response = urllib.request.urlopen(
                    url, 
                    timeout=5,
                    context=urllib.request._create_unverified_context()
                )
                if response.status == 200:
                    print(f"{Colors.GREEN}✅ {name}服务已就绪 ({attempt}/{max_attempts}){Colors.RESET}")
                    self.results[name] = True
                    return True
            except Exception as e:
                if attempt < max_attempts:
                    print(f"{Colors.YELLOW}⏳ {name}服务启动中... ({attempt}/{max_attempts}){Colors.RESET}")
                    time.sleep(self.interval)
                else:
                    print(f"{Colors.RED}❌ {name}服务检查失败: {str(e)}{Colors.RESET}")
                    self.results[name] = False
        
        return False
    
    def parallel_check(self, services: Dict[str, str]) -> Dict[str, bool]:
        """并行检查多个服务"""
        threads = []
        
        for name, url in services.items():
            thread = threading.Thread(
                target=self.check_service, 
                args=(name, url)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        return self.results

class BrowserOpener:
    """浏览器打开器"""
    
    def __init__(self):
        self.browser = self._detect_browser()
    
    def _detect_browser(self) -> str:
        """检测默认浏览器"""
        try:
            import webbrowser
            webbrowser.get()
            return "default"
        except:
            return "chrome"  # 默认使用Chrome
    
    def open(self, url: str, delay: int = 2):
        """打开浏览器"""
        print(f"{Colors.CYAN}🌐 即将打开浏览器: {url}{Colors.RESET}")
        time.sleep(delay)  # 等待前端完全启动
        
        try:
            import webbrowser
            webbrowser.open(url, new=2)  # new=2 在新标签页打开
            print(f"{Colors.GREEN}✅ 浏览器已打开{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  无法自动打开浏览器: {str(e)}{Colors.RESET}")
            print(f"{Colors.CYAN}请手动访问: {url}{Colors.RESET}")

class ProjectStarter:
    """项目启动器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.project_dir = Path(config['project_name'])
        self.db_executor = DatabaseExecutor(config['database'])
        self.service_monitor = ServiceMonitor()
        self.browser_opener = BrowserOpener()
        self.backend_port = config['server']['backend_port']
        self.frontend_port = config['server']['frontend_port']
    
    def start(self):
        """启动项目"""
        print(f"{Colors.BOLD}{Colors.CYAN}🚀 开始启动项目: {self.config['project_name']}{Colors.RESET}")
        
        steps = [
            self.step_validate_environment,
            self.step_check_ports,
            self.step_test_database_connection,
            self.step_execute_sql,
            self.step_build_backend,
            self.step_build_frontend,
            self.step_start_redis,
            self.step_start_backend,
            self.step_start_frontend,
            self.step_monitor_services,
            self.step_open_browser,
        ]
        
        for step in steps:
            try:
                result = step()
                if not result:
                    print(f"{Colors.RED}❌ 步骤失败，停止启动{Colors.RESET}")
                    return False
            except Exception as e:
                print(f"{Colors.RED}❌ 步骤异常: {str(e)}{Colors.RESET}")
                return False
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 项目启动成功！{Colors.RESET}")
        self._print_summary()
        return True
    
    def step_validate_environment(self) -> bool:
        """验证环境"""
        print(f"\n{Colors.BOLD}📋 步骤 1/11 - 验证环境{Colors.RESET}")
        
        checks = [
            ("Java", "java -version", "java"),
            ("Maven", "mvn -v", "mvn"),
            ("Node.js", "node --version", "node"),
            ("NPM", "npm --version", "npm"),
        ]
        
        optional_checks = [
            ("Docker", "docker --version", "docker"),
            ("MySQL Client", "mysql --version", "mysql"),
        ]
        
        all_passed = True
        for name, cmd, check_str in checks:
            try:
                result = subprocess.run(
                    cmd.split(), 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                if check_str in result.stdout.lower() or check_str in result.stderr.lower():
                    print(f"{Colors.GREEN}✅ {name} 已安装{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}⚠️  {name} 版本检查失败{Colors.RESET}")
            except:
                print(f"{Colors.RED}❌ {name} 未找到或无法执行{Colors.RESET}")
                all_passed = False
        
        # 可选依赖检查（警告而非错误）
        for name, cmd, check_str in optional_checks:
            try:
                result = subprocess.run(
                    cmd.split(), 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if check_str in result.stdout.lower() or check_str in result.stderr.lower():
                    print(f"{Colors.GREEN}ℹ️  {name} 已安装 (可选){Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}ℹ️  {name} 未安装 (可选，不影响核心功能){Colors.RESET}")
            except:
                print(f"{Colors.YELLOW}ℹ️  {name} 未安装 (可选，不影响核心功能){Colors.RESET}")
        
        return all_passed
    
    def step_check_ports(self) -> bool:
        """检查端口"""
        print(f"\n{Colors.BOLD}🔌 步骤 2/11 - 检查端口占用{Colors.RESET}")
        
        def is_port_in_use(port: int) -> bool:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', port))
                    return False
                except:
                    return True
        
        ports_to_check = [
            ("后端", self.backend_port),
            ("前端", self.frontend_port),
        ]
        
        all_free = True
        for name, port in ports_to_check:
            if is_port_in_use(port):
                print(f"{Colors.RED}❌ {name}端口 {port} 被占用{Colors.RESET}")
                all_free = False
            else:
                print(f"{Colors.GREEN}✅ {name}端口 {port} 可用{Colors.RESET}")
        
        return all_free
    
    def step_test_database_connection(self) -> bool:
        """测试数据库连接"""
        print(f"\n{Colors.BOLD}🗄️  步骤 3/11 - 测试数据库连接{Colors.RESET}")
        
        success, message = self.db_executor.test_connection()
        if success:
            print(f"{Colors.GREEN}✅ 数据库连接成功{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ {message}{Colors.RESET}")
        
        return success
    
    def step_execute_sql(self) -> bool:
        """执行SQL"""
        print(f"\n{Colors.BOLD}📊 步骤 4/11 - 执行数据库初始化{Colors.RESET}")
        
        sql_file = self.project_dir / "backend" / "src" / "main" / "resources" / "db" / "init.sql"
        success, errors = self.db_executor.execute_sql_file(sql_file)
        
        if success:
            print(f"{Colors.GREEN}✅ 数据库初始化完成{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ 数据库初始化失败{Colors.RESET}")
            for error in errors:
                print(f"{Colors.RED}   - {error}{Colors.RESET}")
        
        return success
    
    def step_build_backend(self) -> bool:
        """构建后端"""
        print(f"\n{Colors.BOLD}🔧 步骤 5/11 - 构建后端项目{Colors.RESET}")
        
        backend_dir = self.project_dir / "backend"
        
        # 检查是否已经构建过
        target_dir = backend_dir / "target"
        if target_dir.exists() and any(target_dir.glob("*.jar")):
            print(f"{Colors.YELLOW}⚠️  检测到已构建的JAR包，跳过构建{Colors.RESET}")
            return True
        
        try:
            # Maven构建
            cmd = ["mvn", "clean", "package", "-DskipTests", "-q"]
            result = subprocess.run(
                cmd, 
                cwd=backend_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                print(f"{Colors.GREEN}✅ 后端构建成功{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}❌ 后端构建失败{Colors.RESET}")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}❌ 后端构建超时{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}❌ 后端构建异常: {str(e)}{Colors.RESET}")
            return False
    
    def step_build_frontend(self) -> bool:
        """构建前端"""
        print(f"\n{Colors.BOLD}📦 步骤 6/11 - 安装前端依赖{Colors.RESET}")
        
        frontend_dir = self.project_dir / "frontend"
        
        # 检查node_modules
        node_modules = frontend_dir / "node_modules"
        if node_modules.exists():
            print(f"{Colors.YELLOW}⚠️  检测到node_modules，跳过安装{Colors.RESET}")
            return True
        
        try:
            # 使用国内镜像源
            cmd = ["npm", "install", "--registry=https://registry.npmmirror.com"]
            result = subprocess.run(
                cmd,
                cwd=frontend_dir,
                capture_output=True,
                text=True,
                timeout=180  # 3分钟超时
            )
            
            if result.returncode == 0:
                print(f"{Colors.GREEN}✅ 前端依赖安装成功{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}❌ 前端依赖安装失败{Colors.RESET}")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}❌ 前端依赖安装超时{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}❌ 前端依赖安装异常: {str(e)}{Colors.RESET}")
            return False
    
    def step_start_redis(self) -> bool:
        """Redis外部服务检查"""
        print(f"\n{Colors.BOLD}🔴 步骤 7/11 - Redis外部服务检查{Colors.RESET}")
        
        redis_config = self.config.get('redis', {})
        if not redis_config.get('enable', True):
            print(f"{Colors.YELLOW}⚠️  Redis已禁用，跳过检查{Colors.RESET}")
            return True
        
        host = redis_config.get('host', 'localhost')
        port = redis_config.get('port', 6379)
        
        print(f"{Colors.CYAN}ℹ️  Redis配置: {host}:{port} (外部服务){Colors.RESET}")
        print(f"{Colors.GREEN}✅ Redis外部服务配置已确认{Colors.RESET}")
        print(f"{Colors.YELLOW}💡 提示: 请确保外部Redis服务已启动{Colors.RESET}")
        
        return True
    
    def step_start_backend(self) -> bool:
        """启动后端"""
        print(f"\n{Colors.BOLD}🚀 步骤 8/11 - 启动后端服务{Colors.RESET}")
        
        backend_dir = self.project_dir / "backend"
        jar_files = list(backend_dir.glob("target/*.jar"))
        
        if not jar_files:
            print(f"{Colors.RED}❌ 未找到JAR包{Colors.RESET}")
            return False
        
        jar_file = jar_files[0]
        
        try:
            # 启动后端服务
            cmd = f"start /B java -jar {jar_file} --server.port={self.backend_port}"
            subprocess.run(cmd, shell=True, cwd=backend_dir)
            
            print(f"{Colors.GREEN}✅ 后端服务已启动 (端口: {self.backend_port}){Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ 后端启动失败: {str(e)}{Colors.RESET}")
            return False
    
    def step_start_frontend(self) -> bool:
        """启动前端"""
        print(f"\n{Colors.BOLD}🎨 步骤 9/11 - 启动前端服务{Colors.RESET}")
        
        frontend_dir = self.project_dir / "frontend"
        
        try:
            # 启动前端开发服务器
            cmd = f"start /B npm run dev -- --port {self.frontend_port}"
            subprocess.run(cmd, shell=True, cwd=frontend_dir)
            
            print(f"{Colors.GREEN}✅ 前端服务已启动 (端口: {self.frontend_port}){Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ 前端启动失败: {str(e)}{Colors.RESET}")
            return False
    
    def step_monitor_services(self) -> bool:
        """监控服务"""
        print(f"\n{Colors.BOLD}👀 步骤 10/11 - 监控服务状态{Colors.RESET}")
        
        time.sleep(5)  # 等待服务初始化
        
        services = {
            "后端": f"http://localhost:{self.backend_port}/api/health",
            "前端": f"http://localhost:{self.frontend_port}",
        }
        
        results = self.service_monitor.parallel_check(services)
        
        all_ready = all(results.values())
        if all_ready:
            print(f"{Colors.GREEN}✅ 所有服务已就绪{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ 部分服务未就绪{Colors.RESET}")
            for name, ready in results.items():
                status = "✅" if ready else "❌"
                print(f"   {status} {name}: {'已就绪' if ready else '未就绪'}")
        
        return all_ready
    
    def step_open_browser(self) -> bool:
        """打开浏览器"""
        print(f"\n{Colors.BOLD}🌐 步骤 11/11 - 打开浏览器{Colors.RESET}")
        
        login_url = f"http://localhost:{self.frontend_port}/login"
        self.browser_opener.open(login_url)
        
        return True
    
    def _print_summary(self):
        """打印启动摘要"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 启动摘要{Colors.RESET}")
        print(f"{Colors.CYAN}📍 后端API: http://localhost:{self.backend_port}/api{Colors.RESET}")
        print(f"{Colors.CYAN}📍 前端页面: http://localhost:{self.frontend_port}{Colors.RESET}")
        print(f"{Colors.CYAN}📍 Swagger文档: http://localhost:{self.backend_port}/api/swagger-ui{Colors.RESET}")
        print(f"{Colors.CYAN}🔑 默认账号: admin / 123456{Colors.RESET}")
        print(f"{Colors.CYAN}📁 项目目录: {self.project_dir.absolute()}{Colors.RESET}")
        print(f"\n{Colors.YELLOW}💡 提示: 使用 Ctrl+C 停止所有服务{Colors.RESET}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python optimized-start.py <config.json>")
        sys.exit(1)
    
    # 加载配置文件
    config_file = Path(sys.argv[1])
    if not config_file.exists():
        print(f"配置文件不存在: {config_file}")
        sys.exit(1)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 启动项目
    starter = ProjectStarter(config)
    success = starter.start()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()