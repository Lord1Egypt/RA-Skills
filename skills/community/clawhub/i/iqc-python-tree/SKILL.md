name: iqc-python-tree
version: 3.0.0

description: |
  企业工业级 IQC 控制计划解析引擎终极稳定版：
  Excel → CSV → JSON AST → 安全认证 → 数据提交

author: inspection-planning

# ===============================
# 模型推理参数（低随机性工业模式）
# ===============================

model:
  temperature: 0
  top_p: 0.05

# ===============================
# 工作流执行模式（稳定核心）
# 顺序执行，不使用复杂调度器
# ===============================

workflow:

  steps:

    # --------------------------------------------------
    # Step 1：Excel 工业预处理层（核心稳定区）
    # --------------------------------------------------
    - name: preprocess-excel
      executor: python
      script: scripts/preprocess_excel.py
      timeout: 120
      retry: 2
      params:
        input_dir: ./input
        output_dir: ./output/csv

    # --------------------------------------------------
    # Step 2：工业语义解析层（控制计划模型化）
    # --------------------------------------------------
    - name: csv-to-json-parser
      executor: python
      script: scripts/csv_to_json.py
      timeout: 180
      retry: 3
      params:
        input_dir: ./output/csv
        output_dir: ./output/json

    # --------------------------------------------------
    # Step 3：安全认证层（企业安全标准）
    # --------------------------------------------------
    - name: jwt-security-layer
      executor: python
      script: scripts/jwt_token.py
      timeout: 60
      retry: 2
      params:
        secret_key: STATIC_SECRET_KEY
        expire_minutes: 30

    # --------------------------------------------------
    # Step 4：工业数据提交层（最终出口）
    # --------------------------------------------------
    - name: enterprise-data-submit
      executor: python
      script: scripts/data_submit.py
      timeout: 120
      retry: 3
      params:
        auth_mode: BearerToken

# ===============================
# 企业异常自愈策略（非常重要）
# ===============================

error_strategy:

  global_retry: 3

  fallback_mode: safe_exit

  handlers:
    - log_error
    - save_checkpoint
    - alert_admin

# ===============================
# 日志审计系统（工业生产必须）
# ===============================

logging:

  level: INFO
  persist: true
  path: ./logs/iqc_engine.log

# ===============================
# 输出策略
# ===============================

output:

  format: json
  path: ./output/final
  compress: true