"""
OCAX Passport - 节点身份证生成器 (最终版)
Node Identity Card Generator (Final)
"""

import os
import socket
import platform
import json
import uuid
import psutil
import datetime
import subprocess
from typing import Dict, Any, Optional, List
from threading import Thread
import time


class HardwareScorer:
    """硬件评分器"""
    
    # 任务类型权重配置
    TASK_WEIGHTS = {
        "general_computation": {"cpu": 0.5, "memory": 0.3, "gpu": 0.1, "storage": 0.1},
        "image_processing": {"cpu": 0.3, "memory": 0.3, "gpu": 0.3, "storage": 0.1},
        "video_processing": {"cpu": 0.3, "memory": 0.3, "gpu": 0.3, "storage": 0.1},
        "ai_inference": {"cpu": 0.1, "memory": 0.2, "gpu": 0.6, "storage": 0.1},
        "data_processing": {"cpu": 0.4, "memory": 0.4, "gpu": 0.1, "storage": 0.1},
        "3d_rendering": {"cpu": 0.2, "memory": 0.3, "gpu": 0.4, "storage": 0.1},
        "audio_processing": {"cpu": 0.4, "memory": 0.3, "gpu": 0.1, "storage": 0.2}
    }
    
    @classmethod
    def score_cpu(cls, cpu_info: Dict) -> float:
        """CPU 评分"""
        score = 0
        
        # 核心数评分 (最高40分)
        cores = cpu_info.get("cores_physical", 1)
        if cores >= 16:
            score += 40
        elif cores >= 8:
            score += 30
        elif cores >= 4:
            score += 20
        else:
            score += 10
        
        # 线程数加分 (最高20分)
        threads = cpu_info.get("cores_logical", 1)
        if threads >= 32:
            score += 20
        elif threads >= 16:
            score += 15
        elif threads >= 8:
            score += 10
        
        # 频率评分 (最高20分)
        freq = cpu_info.get("frequency_current", "0")
        try:
            freq_mhz = float(freq.replace(" MHz", ""))
            if freq_mhz >= 4000:
                score += 20
            elif freq_mhz >= 3000:
                score += 15
            elif freq_mhz >= 2000:
                score += 10
        except:
            pass
        
        # 使用率 (最高20分，负载低分数高)
        usage = cpu_info.get("usage_percent", 100)
        if usage < 20:
            score += 20
        elif usage < 50:
            score += 15
        elif usage < 80:
            score += 10
        
        return min(100, score)
    
    @classmethod
    def score_gpu(cls, gpus: List[Dict]) -> float:
        """GPU 评分"""
        if not gpus or "Integrated" in gpus[0].get("name", ""):
            return 10  # 集成显卡低分
        
        score = 0
        for gpu in gpus:
            name = gpu.get("name", "").lower()
            
            # 检测显卡型号
            if "rtx 5090" in name or "rtx 4090" in name:
                score = 100
            elif "rtx 5080" in name or "rtx 4080" in name:
                score = 90
            elif "rtx 5070" in name or "rtx 4070" in name:
                score = 80
            elif "rtx 5060" in name or "rtx 4060" in name:
                score = 70
            elif "rtx 3090" in name or "rtx 3080" in name:
                score = 85
            elif "rtx 2080" in name or "rtx 2070" in name:
                score = 60
            elif "gtx 1080" in name or "gtx 1070" in name:
                score = 50
            elif "radeon" in name:
                if "rx 7900" in name:
                    score = 85
                elif "rx 6900" in name:
                    score = 75
                else:
                    score = 40
            else:
                score = 30
            
            # 显存加分
            mem = gpu.get("memory_total", "")
            if "MiB" in mem:
                try:
                    mem_gb = int(mem.replace(" MiB", "")) / 1024
                    if mem_gb >= 24:
                        score += 10
                    elif mem_gb >= 12:
                        score += 7
                    elif mem_gb >= 8:
                        score += 5
                except:
                    pass
        
        return min(100, score)
    
    @classmethod
    def score_memory(cls, mem_info: Dict) -> float:
        """内存评分"""
        score = 0
        
        # 内存大小评分
        total = mem_info.get("total", "0 GB")
        try:
            gb = float(total.replace(" GB", ""))
            if gb >= 64:
                score = 100
            elif gb >= 32:
                score = 80
            elif gb >= 16:
                score = 60
            elif gb >= 8:
                score = 40
            else:
                score = 20
        except:
            score = 10
        
        # 可用内存加分
        avail = mem_info.get("available", "0 GB")
        try:
            avail_gb = float(avail.replace(" GB", ""))
            if avail_gb >= 32:
                score += 10
            elif avail_gb >= 16:
                score += 7
            elif avail_gb >= 8:
                score += 5
        except:
            pass
        
        return min(100, score)
    
    @classmethod
    def score_storage(cls, storage: List[Dict]) -> float:
        """存储评分"""
        if not storage:
            return 10
        
        total_score = 0
        count = 0
        
        for disk in storage:
            score = 0
            
            # 容量评分
            total = disk.get("total", "0 GB")
            try:
                gb = float(total.replace(" GB", ""))
                if gb >= 2000:  # 2TB+
                    score = 100
                elif gb >= 1000:  # 1TB
                    score = 80
                elif gb >= 500:
                    score = 60
                elif gb >= 256:
                    score = 40
                else:
                    score = 20
            except:
                score = 10
            
            # 剩余空间加分
            free = disk.get("free", "0 GB")
            try:
                free_gb = float(free.replace(" GB", ""))
                if free_gb >= 500:
                    score += 10
                elif free_gb >= 200:
                    score += 7
                elif free_gb >= 100:
                    score += 5
            except:
                pass
            
            total_score += score
            count += 1
        
        return min(100, total_score // count if count else 10)
    
    @classmethod
    def score_os(cls, os_info: Dict) -> float:
        """操作系统评分"""
        system = os_info.get("system", "").lower()
        
        if system == "windows":
            # Windows 11 评分更高
            version = os_info.get("version", "")
            if "10.0.2" in version or "10.0.2" in version:  # Win11
                return 90
            return 70
        elif system == "linux":
            return 85
        elif system == "darwin":
            return 95
        else:
            return 50
    
    @classmethod
    def calculate_overall_score(cls, hardware: Dict, task_type: str = "general_computation") -> Dict[str, float]:
        """计算综合评分"""
        weights = cls.TASK_WEIGHTS.get(task_type, cls.TASK_WEIGHTS["general_computation"])
        
        cpu = cls.score_cpu(hardware.get("cpu", {}))
        gpu = cls.score_gpu(hardware.get("gpu", []))
        memory = cls.score_memory(hardware.get("memory", {}))
        storage = cls.score_storage(hardware.get("storage", []))
        os_score = cls.score_os(hardware.get("os", {}))
        
        # 加权计算
        task_score = (
            cpu * weights["cpu"] +
            gpu * weights["gpu"] +
            memory * weights["memory"] +
            storage * weights["storage"]
        )
        
        # 整体评分 (任务评分 + 操作系统)
        overall = task_score * 0.9 + os_score * 0.1
        
        return {
            "overall_score": round(overall, 1),
            "task_score": round(task_score, 1),
            "cpu_score": cpu,
            "gpu_score": gpu,
            "memory_score": memory,
            "storage_score": storage,
            "os_score": os_score,
            "task_type": task_type,
            "weights_used": weights
        }


class NodePassport:
    """节点护照/身份证 (最终版)"""
    
    def __init__(self):
        self.passport_id = ""
        self.node_name = ""
        self.node_id = ""
        self.owner_name = ""
        self.created_at = ""
        self.updated_at = ""
        
        self.hardware = {}
        self.reputation = {"score": 100.0, "completed_tasks": 0, "success_rate": 100.0, "uptime_hours": 0}
        self.supported_tasks = []
        self.task_requirements = {}
        
        # 综合评分
        self.scores = {}
        
        # 自动更新
        self.auto_update_enabled = False
        self.update_interval = 86400  # 24小时
        self._update_thread = None
    
    def generate(self, node_name: str = None, owner_name: str = None) -> "NodePassport":
        """生成节点护照"""
        import uuid as uuid_lib
        
        self.passport_id = f"OCAX-PASSPORT-{datetime.datetime.now().strftime('%Y%m%d')}-{str(uuid_lib.uuid4())[:8]}"
        self.node_id = f"OCAX-NODE-{datetime.datetime.now().strftime('%Y%m%d')}-{str(uuid_lib.uuid4())[:8]}"
        self.node_name = node_name or socket.gethostname()
        self.owner_name = owner_name or "Anonymous"
        self.created_at = datetime.datetime.now().isoformat()
        self.updated_at = self.created_at
        
        self.hardware = self._get_hardware_info()
        self.supported_tasks = self._detect_supported_tasks()
        self.task_requirements = self._get_task_requirements()
        self.scores = self._calculate_all_scores()
        
        return self
    
    def _get_hardware_info(self) -> Dict[str, Any]:
        """获取硬件信息"""
        info = {}
        
        # CPU
        cpu_info = {}
        try:
            cpu_info["model"] = platform.processor() or platform.system()
            cpu_info["cores_physical"] = psutil.cpu_count(logical=False)
            cpu_info["cores_logical"] = psutil.cpu_count(logical=True)
            if psutil.cpu_freq():
                cpu_info["frequency_current"] = f"{psutil.cpu_freq().current:.0f} MHz"
            cpu_info["usage_percent"] = psutil.cpu_percent(interval=1)
        except:
            cpu_info["model"] = "Unknown"
        
        info["cpu"] = cpu_info
        
        # 内存
        mem = psutil.virtual_memory()
        info["memory"] = {
            "total": f"{mem.total / (1024**3):.2f} GB",
            "available": f"{mem.available / (1024**3):.2f} GB",
            "percent": f"{mem.percent}%"
        }
        
        # GPU
        info["gpu"] = self._get_gpu_info()
        
        # 存储
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mount": partition.mountpoint,
                    "total": f"{usage.total / (1024**3):.2f} GB",
                    "free": f"{usage.free / (1024**3):.2f} GB",
                    "percent": f"{usage.percent}%"
                })
            except:
                pass
        info["storage"] = disks[:5]
        
        # OS
        info["os"] = {"system": platform.system(), "release": platform.release(), "version": platform.version()}
        
        return info
    
    def _get_gpu_info(self) -> List[Dict]:
        """获取GPU信息"""
        gpus = []
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = [p.strip() for p in line.split(',')]
                        if parts:
                            gpus.append({"name": parts[0], "memory_total": parts[1] if len(parts) > 1 else "Unknown"})
        except:
            pass
        return gpus if gpus else [{"name": "Integrated Graphics"}]
    
    def _detect_supported_tasks(self) -> List[Dict]:
        """检测支持的任务"""
        tasks = []
        cpu_cores = psutil.cpu_count(logical=False) or 1
        mem_gb = psutil.virtual_memory().total / (1024**3)
        gpus = self._get_gpu_info()
        has_gpu = len(gpus) > 0 and "Integrated" not in gpus[0].get("name", "")
        
        all_tasks = [
            ("general_computation", "通用计算", "low"),
            ("image_processing", "图像处理", mem_gb >= 4),
            ("video_processing", "视频处理", mem_gb >= 8),
            ("ai_inference", "AI推理", has_gpu and mem_gb >= 8),
            ("data_processing", "数据处理", cpu_cores >= 2),
            ("3d_rendering", "3D渲染", has_gpu),
            ("audio_processing", "音频处理", mem_gb >= 4)
        ]
        
        for task_type, name, condition in all_tasks:
            status = "available" if condition else "unavailable"
            tasks.append({"type": task_type, "name": name, "status": status})
        
        return tasks
    
    def _get_task_requirements(self) -> Dict[str, Dict]:
        """任务资源需求"""
        return {
            "general_computation": {"cpu_cores": 1, "memory_gb": 1},
            "image_processing": {"cpu_cores": 2, "memory_gb": 4},
            "video_processing": {"cpu_cores": 8, "memory_gb": 16},
            "ai_inference": {"cpu_cores": 4, "memory_gb": 8, "gpu": "required"},
            "data_processing": {"cpu_cores": 4, "memory_gb": 8},
            "3d_rendering": {"cpu_cores": 8, "memory_gb": 16, "gpu": "required"},
            "audio_processing": {"cpu_cores": 1, "memory_gb": 2}
        }
    
    def _calculate_all_scores(self) -> Dict[str, Any]:
        """计算所有任务类型的评分"""
        scores = {}
        
        for task_type in HardwareScorer.TASK_WEIGHTS.keys():
            scores[task_type] = HardwareScorer.calculate_overall_score(self.hardware, task_type)
        
        # 最佳任务类型
        best_task = max(scores.items(), key=lambda x: x[1]["task_score"])
        
        return {
            "by_task": scores,
            "best_task": best_task[0],
            "best_score": best_task[1]["task_score"]
        }
    
    def update_hardware_info(self):
        """更新硬件信息"""
        self.hardware = self._get_hardware_info()
        self.supported_tasks = self._detect_supported_tasks()
        self.scores = self._calculate_all_scores()
        self.updated_at = datetime.datetime.now().isoformat()
    
    def enable_auto_update(self, interval_seconds: int = 86400):
        """启用自动更新 (默认24小时)"""
        self.auto_update_enabled = True
        self.update_interval = interval_seconds
        
        def _auto_update():
            while self.auto_update_enabled:
                time.sleep(self.update_interval)
                if self.auto_update_enabled:
                    self.update_hardware_info()
        
        self._update_thread = Thread(target=_auto_update, daemon=True)
        self._update_thread.start()
    
    def disable_auto_update(self):
        """禁用自动更新"""
        self.auto_update_enabled = False
    
    def to_json(self) -> Dict:
        """转换为 JSON"""
        return {
            "passport_id": self.passport_id,
            "node_id": self.node_id,
            "node_name": self.node_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "hardware": self.hardware,
            "reputation": self.reputation,
            "supported_tasks": self.supported_tasks,
            "scores": self.scores,
            "auto_update": self.auto_update_enabled
        }


def generate_passport(node_name: str = None, owner_name: str = None) -> NodePassport:
    """生成节点护照"""
    passport = NodePassport()
    return passport.generate(node_name, owner_name)


if __name__ == "__main__":
    print("=" * 60)
    print("OCAX Passport (Final)")
    print("=" * 60)
    
    passport = generate_passport("My-PC", "User")
    
    print("\n[Hardware Scores]")
    scores = passport.scores["by_task"]
    for task, data in scores.items():
        print(f"  {task}: {data['task_score']:.1f}")
    
    print(f"\n[Best Task]: {passport.scores['best_task']} ({passport.scores['best_score']:.1f})")
    
    print("\n[Auto Update]")
    passport.enable_auto_update(60)  # 60秒测试
    print(f"  Enabled: {passport.auto_update_enabled}")
    print(f"  Interval: {passport.update_interval}s")
    
    print("\n[JSON Summary]")
    print(json.dumps(passport.to_json(), indent=2)[:500])
