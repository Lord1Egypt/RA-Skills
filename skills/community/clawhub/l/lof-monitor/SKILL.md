
## 工具介绍：
这是一个股票金融投资（A股）LOF基金的套利监控工具，通过遍历LOF基金的场内和场外差价发现套利机会。当溢价或折价超过脚本设置的阈值（默认为10％），工具会监控到并输出。

## 安装依赖
python -m pip install requirements.txt

## 工具使用
python LOFMonitor.py

## 获取结果
待脚本执行结束（预计运行时间约30秒），直接读取LOFMonitor_output.txt文件内容，并输出。