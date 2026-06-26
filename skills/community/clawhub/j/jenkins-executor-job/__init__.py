import json
from pathlib import Path
from openclaw.sdk import BaseSkill, Context
from jenkinsapi.jenkins import Jenkins

class JenkinsExecutorSkill(BaseSkill):
    def __init__(self):
        super().__init__()
        self.jenkins = None
        self.config = None
        self.skill_name = "jenkins-executor"

    def init(self):
        """初始化：加载配置 + 连接 Jenkins"""
        try:
            # 加载配置文件
            config_path = Path(__file__).parent / "config.json"
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)

            # 连接 Jenkins
            self.jenkins = Jenkins(
                baseurl=self.config["base_url"],
                username=self.config["username"],
                password=self.config["api_token"],
                timeout=30
            )
            self.logger.info("[Jenkins Skill] 初始化成功，已连接 Jenkins")
        except Exception as e:
            self.logger.error(f"[Jenkins Skill] 初始化失败: {str(e)}")
            raise

    def get_tools(self):
        """暴露给 OpenClaw 的所有工具"""
        return [
            {
                "name": "jenkins.job.list",
                "description": "查询 Jenkins 所有任务列表",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "jenkins.build.trigger",
                "description": "触发 Jenkins 任务构建",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "jobName": {"type": "string", "description": "任务名称"},
                        "params": {"type": "object", "description": "构建参数（可选）"}
                    },
                    "required": ["jobName"]
                }
            },
            {
                "name": "jenkins.build.status",
                "description": "查询任务最新构建状态",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "jobName": {"type": "string", "description": "任务名称"}
                    },
                    "required": ["jobName"]
                }
            },
            {
                "name": "jenkins.build.log",
                "description": "获取构建日志",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "jobName": {"type": "string", "description": "任务名称"},
                        "buildNumber": {"type": "number", "description": "构建编号（默认最新）"}
                    },
                    "required": ["jobName"]
                }
            },
            {
                "name": "jenkins.build.stop",
                "description": "停止正在运行的构建",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "jobName": {"type": "string", "description": "任务名称"},
                        "buildNumber": {"type": "number", "description": "构建编号"}
                    },
                    "required": ["jobName", "buildNumber"]
                }
            }
        ]

    def execute(self, context: Context):
        """执行工具逻辑"""
        tool_name = context.tool_name
        params = context.params

        try:
            if tool_name == "jenkins.job.list":
                return self.get_job_list()

            elif tool_name == "jenkins.build.trigger":
                return self.trigger_build(params.get("jobName"), params.get("params", {}))

            elif tool_name == "jenkins.build.status":
                return self.get_build_status(params.get("jobName"))

            elif tool_name == "jenkins.build.log":
                return self.get_build_log(params.get("jobName"), params.get("buildNumber"))

            elif tool_name == "jenkins.build.stop":
                return self.stop_build(params.get("jobName"), params.get("buildNumber"))

            else:
                return {"success": False, "error": f"不支持的工具: {tool_name}"}

        except Exception as e:
            self.logger.error(f"执行失败: {str(e)}")
            return {
                "success": False,
                "message": "Jenkins 操作失败",
                "error": str(e)
            }

    # ==================== 1. 查询任务列表 ====================
    def get_job_list(self):
        """获取所有 Jenkins 任务"""
        jobs = self.jenkins.get_jobs()
        job_list = []

        for job in jobs:
            job_list.append({
                "name": job.name,
                "url": job.url,
                "type": job.get_build_class().__name__ if job.get_build_class() else "Unknown"
            })

        return {
            "success": True,
            "total": len(job_list),
            "jobs": job_list
        }

    # ==================== 2. 触发构建 ====================
    def trigger_build(self, job_name: str, params: dict):
        """触发 Jenkins 任务构建"""
        job = self.jenkins.get_job(job_name)
        if params:
            job.invoke(build_params=params)
        else:
            job.invoke()

        return {
            "success": True,
            "message": "构建已触发",
            "jobName": job_name
        }

    # ==================== 3. 查询构建状态 ====================
    def get_build_status(self, job_name: str):
        """查询任务最新构建状态"""
        job = self.jenkins.get_job(job_name)
        last_build = job.get_last_build_or_none()

        if not last_build:
            return {"success": True, "message": "暂无构建记录", "jobName": job_name}

        return {
            "success": True,
            "jobName": job_name,
            "buildNumber": last_build.get_number(),
            "status": last_build.get_status() or "BUILDING",
            "url": last_build.get_url(),
            "isRunning": last_build.is_running()
        }

    # ==================== 4. 获取构建日志 ====================
    def get_build_log(self, job_name: str, build_number=None):
        """获取构建日志"""
        job = self.jenkins.get_job(job_name)

        if not build_number:
            build = job.get_last_build_or_none()
            if not build:
                return {"success": False, "error": "无构建记录"}
        else:
            build = job.get_build(build_number)

        log = build.get_console()[-3000:]  # 截取最后 3000 字符
        return {
            "success": True,
            "jobName": job_name,
            "buildNumber": build.get_number(),
            "log": log
        }

    # ==================== 5. 停止构建 ====================
    def stop_build(self, job_name: str, build_number: int):
        """停止运行中的构建"""
        job = self.jenkins.get_job(job_name)
        build = job.get_build(build_number)
        build.stop()

        return {
            "success": True,
            "message": "构建已停止",
            "jobName": job_name,
            "buildNumber": build_number
        }

    def destroy(self):
        """销毁资源"""
        self.logger.info("[Jenkins Skill] 已销毁")