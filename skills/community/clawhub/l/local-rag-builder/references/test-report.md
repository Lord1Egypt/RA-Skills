## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | local-rag-builder |
| 测试时间 | 2026-06-21 18:06 |
| 测试轮次 | 3 |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 4 | 4 | 0 | 100% |
| D1-D6 功能测试 | 426 | 293 | 0 | 68% |
| S4 执行忠实度 | 21 | 21 | - | 100% |
| S4 综合评分 | - | N/A | - | 60% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S2 | INFO | 「配置加载与保存」 | PASS | config 导入成功 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 7 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\config.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\embedding_model_ | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\knowledge_base_m | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\prompt_manager.p | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\rag_core.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\rag_env_setup.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\rag_setup_orches | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\rag_skill.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\rag_standalone.p | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\rag_web_ui.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\reranker.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\router.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\text_splitter.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\utils.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\embedding_model_m | PASS | :0 | exit code 0, stdout 649 chars |
| D1 | INFO | 运行时: scripts\knowledge_base_ma | PASS | :0 | exit code 0, stdout 1136 chars |
| D1 | INFO | 运行时: scripts\prompt_manager.py | PASS | :0 | exit code 0, stdout 423 chars |
| D1 | INFO | 运行时: scripts\rag_env_setup.py  | PASS | :0 | exit code 0, stdout 788 chars |
| D1 | INFO | 运行时: scripts\rag_setup_orchest | PASS | :0 | exit code 0, stdout 426 chars |
| D1 | INFO | 运行时: scripts\rag_skill.py --he | PASS | :0 | exit code 0, stdout 816 chars |
| D1 | INFO | 运行时: scripts\rag_standalone.py | PASS | :0 | exit code 0, stdout 650 chars |
| D1 | INFO | 运行时: scripts\rag_web_ui.py --h | PASS | :0 | exit code 0, stdout 236 chars |
| D1 | INFO | 运行时: scripts\reranker.py --hel | PASS | :0 | exit code 0, stdout 496 chars |
| D1 | INFO | 运行时: scripts\router.py --help | PASS | :0 | exit code 0, stdout 407 chars |
| D1 | INFO | 运行时: scripts\text_splitter.py  | PASS | :0 | exit code 0, stdout 925 chars |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\config.py → utils.cfg_dir |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\config.py → utils.safe_json_load |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\config.py → utils.safe_json_dump |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\embedding_model_manager.py → utils.MODELS_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\embedding_model_manager.py → utils.cache_d |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\embedding_model_manager.py → utils.run_com |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\embedding_model_manager.py → utils.dir_siz |
| D2 | INFO | 外部依赖: huggingface_hub | PASS | :0 | scripts\embedding_model_manager.py → huggingface_h |
| D2 | INFO | 外部依赖: huggingface_hub | PASS | :0 | scripts\embedding_model_manager.py → huggingface_h |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\embedding_model_manager.py → time |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\embedding_model_manager.py → argparse |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\knowledge_base_manager.py → glob |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\knowledge_base_manager.py → utils.KB_DIR |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\knowledge_base_manager.py → utils.safe_jso |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\knowledge_base_manager.py → utils.safe_jso |
| D2 | INFO | 外部依赖: langchain_chroma | PASS | :0 | scripts\knowledge_base_manager.py → langchain_chro |
| D2 | INFO | 外部依赖: langchain_chroma | PASS | :0 | scripts\knowledge_base_manager.py → langchain_chro |
| D2 | INFO | 外部依赖: langchain_community | PASS | :0 | scripts\knowledge_base_manager.py → langchain_comm |
| D2 | INFO | 外部依赖: langchain_core | PASS | :0 | scripts\knowledge_base_manager.py → langchain_core |
| D2 | INFO | 外部依赖: langchain_community | PASS | :0 | scripts\knowledge_base_manager.py → langchain_comm |
| D2 | INFO | 外部依赖: langchain_community | PASS | :0 | scripts\knowledge_base_manager.py → langchain_comm |
| D2 | INFO | 外部依赖: langchain_core | PASS | :0 | scripts\knowledge_base_manager.py → langchain_core |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\knowledge_base_manager.py → argparse |
| D2 | INFO | 外部依赖: langchain_community | PASS | :0 | scripts\knowledge_base_manager.py → langchain_comm |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\prompt_manager.py → utils.PROMPTS_DIR |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\prompt_manager.py → argparse |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_core.py → config.load_config |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\rag_core.py → utils.KB_DIR |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\rag_core.py → utils.MODELS_DIR |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\rag_core.py → utils.find_model_dirs |
| D2 | INFO | 外部依赖: langchain_huggingface | PASS | :0 | scripts\rag_core.py → langchain_huggingface.Huggin |
| D2 | INFO | 外部依赖: torch | PASS | :0 | scripts\rag_core.py → torch |
| D2 | INFO | 外部依赖: langchain_chroma | PASS | :0 | scripts\rag_core.py → langchain_chroma.Chroma |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_core.py → config.load_config |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_core.py → prompt_manager.load_template |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_core.py → prompt_manager.get_default_t |
| D2 | INFO | 外部依赖: text_splitter | PASS | :0 | scripts\rag_core.py → text_splitter.split_pipeline |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_core.py → knowledge_base_manager.add_d |
| D2 | INFO | 外部依赖: router | PASS | :0 | scripts\rag_core.py → router.route_query |
| D2 | INFO | 外部依赖: reranker | PASS | :0 | scripts\rag_core.py → reranker.Reranker |
| D2 | INFO | 外部依赖: langchain_community | PASS | :0 | scripts\rag_core.py → langchain_community.document |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_core.py → knowledge_base_manager.get_k |
| D2 | INFO | 外部依赖: router | PASS | :0 | scripts\rag_core.py → router.update_kb_signature |
| D2 | INFO | 外部依赖: platform | PASS | :0 | scripts\rag_env_setup.py → platform |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\rag_env_setup.py → time |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\rag_env_setup.py → threading |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\rag_env_setup.py → argparse |
| D2 | INFO | 外部依赖: rag_env_setup | PASS | :0 | scripts\rag_setup_orchestrator.py → rag_env_setup. |
| D2 | INFO | 外部依赖: rag_env_setup | PASS | :0 | scripts\rag_setup_orchestrator.py → rag_env_setup. |
| D2 | INFO | 外部依赖: rag_env_setup | PASS | :0 | scripts\rag_setup_orchestrator.py → rag_env_setup. |
| D2 | INFO | 外部依赖: rag_env_setup | PASS | :0 | scripts\rag_setup_orchestrator.py → rag_env_setup. |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_setup_orchestrator.py → embedding_mode |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_setup_orchestrator.py → embedding_mode |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_setup_orchestrator.py → knowledge_base |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_setup_orchestrator.py → knowledge_base |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_setup_orchestrator.py → knowledge_base |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_setup_orchestrator.py → config.save_co |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_setup_orchestrator.py → config.DEFAULT |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_setup_orchestrator.py → config.load_co |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_setup_orchestrator.py → embedding_mode |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_setup_orchestrator.py → knowledge_base |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\rag_setup_orchestrator.py → argparse |
| D2 | INFO | 外部依赖: rag_core | PASS | :0 | scripts\rag_skill.py → rag_core.get_embeddings |
| D2 | INFO | 外部依赖: rag_core | PASS | :0 | scripts\rag_skill.py → rag_core.format_skill_outpu |
| D2 | INFO | 外部依赖: rag_core | PASS | :0 | scripts\rag_skill.py → rag_core.import_documents_t |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_skill.py → knowledge_base_manager.list |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_skill.py → knowledge_base_manager.get_ |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_skill.py → prompt_manager.load_templat |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\rag_skill.py → argparse |
| D2 | INFO | 外部依赖: rag_core | PASS | :0 | scripts\rag_skill.py → rag_core.retrieve_context |
| D2 | INFO | 外部依赖: rag_core | PASS | :0 | scripts\rag_standalone.py → rag_core.get_embedding |
| D2 | INFO | 外部依赖: rag_core | PASS | :0 | scripts\rag_standalone.py → rag_core.retrieve_cont |
| D2 | INFO | 外部依赖: rag_core | PASS | :0 | scripts\rag_standalone.py → rag_core.import_docume |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_standalone.py → config.load_config |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_standalone.py → config.save_config |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_standalone.py → config.reset_config |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_standalone.py → prompt_manager.load_te |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_standalone.py → prompt_manager.save_te |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_standalone.py → prompt_manager.reset_t |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_standalone.py → prompt_manager.get_def |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_standalone.py → prompt_manager.build_p |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_standalone.py → knowledge_base_manager |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_standalone.py → knowledge_base_manager |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_standalone.py → knowledge_base_manager |
| D2 | INFO | 外部依赖: langchain_community | PASS | :0 | scripts\rag_standalone.py → langchain_community.ll |
| D2 | INFO | 外部依赖: urllib | PASS | :0 | scripts\rag_standalone.py → urllib.request |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\rag_standalone.py → argparse |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\rag_web_ui.py → http.server |
| D2 | INFO | 外部依赖: socketserver | PASS | :0 | scripts\rag_web_ui.py → socketserver |
| D2 | INFO | 外部依赖: urllib | PASS | :0 | scripts\rag_web_ui.py → urllib.parse |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\rag_web_ui.py → threading |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\rag_web_ui.py → time |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_web_ui.py → config.load_config |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_web_ui.py → config.save_config |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_web_ui.py → config.reset_config |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\rag_web_ui.py → config.DEFAULT_CONFIG |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_web_ui.py → prompt_manager.load_templa |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_web_ui.py → prompt_manager.save_templa |
| D2 | INFO | 外部依赖: prompt_manager | PASS | :0 | scripts\rag_web_ui.py → prompt_manager.reset_templ |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_web_ui.py → embedding_model_manager.li |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_web_ui.py → embedding_model_manager.RE |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_web_ui.py → embedding_model_manager.do |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.lis |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.get |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.get |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.set |
| D2 | INFO | 外部依赖: router | PASS | :0 | scripts\rag_web_ui.py → router.list_kb_signatures |
| D2 | INFO | 外部依赖: router | PASS | :0 | scripts\rag_web_ui.py → router.rebuild_all_signatu |
| D2 | INFO | 外部依赖: rag_standalone | PASS | :0 | scripts\rag_web_ui.py → rag_standalone.verify_llm_ |
| D2 | INFO | 外部依赖: text_splitter | PASS | :0 | scripts\rag_web_ui.py → text_splitter.STRATEGY_REG |
| D2 | INFO | 外部依赖: text_splitter | PASS | :0 | scripts\rag_web_ui.py → text_splitter.GUARD_REGIST |
| D2 | INFO | 外部依赖: text_splitter | PASS | :0 | scripts\rag_web_ui.py → text_splitter.get_all_stra |
| D2 | INFO | 外部依赖: text_splitter | PASS | :0 | scripts\rag_web_ui.py → text_splitter.SECONDARY_ST |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\rag_web_ui.py → utils.cfg_dir |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_web_ui.py → embedding_model_manager.RE |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_web_ui.py → embedding_model_manager.RE |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\rag_web_ui.py → argparse |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager._lo |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.rem |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.set |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.res |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.set |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.lis |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\rag_web_ui.py → knowledge_base_manager.get |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_web_ui.py → embedding_model_manager.li |
| D2 | INFO | 外部依赖: langchain_community | PASS | :0 | scripts\rag_web_ui.py → langchain_community.llms.O |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_web_ui.py → embedding_model_manager.DO |
| D2 | INFO | 外部依赖: embedding_model_manager | PASS | :0 | scripts\rag_web_ui.py → embedding_model_manager.do |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\rag_web_ui.py → utils.cache_directory |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\reranker.py → config.load_config |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\reranker.py → argparse |
| D2 | INFO | 外部依赖: torch | PASS | :0 | scripts\reranker.py → torch |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\reranker.py → utils.MODELS_DIR |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\reranker.py → utils.find_model_dirs |
| D2 | INFO | 外部依赖: transformers | PASS | :0 | scripts\reranker.py → transformers.AutoModelForSeq |
| D2 | INFO | 外部依赖: transformers | PASS | :0 | scripts\reranker.py → transformers.AutoTokenizer |
| D2 | INFO | 外部依赖: torch | PASS | :0 | scripts\reranker.py → torch |
| D2 | INFO | 外部依赖: langchain_core | PASS | :0 | scripts\reranker.py → langchain_core.documents.Doc |
| D2 | INFO | 外部依赖: config | PASS | :0 | scripts\router.py → config.load_config |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\router.py → utils.KB_DIR |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\router.py → utils.safe_json_load |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\router.py → utils.safe_json_dump |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\router.py → knowledge_base_manager._load_r |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\router.py → knowledge_base_manager.auto_cl |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\router.py → knowledge_base_manager.list_kn |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\router.py → knowledge_base_manager._load_i |
| D2 | INFO | 外部依赖: knowledge_base_manager | PASS | :0 | scripts\router.py → knowledge_base_manager.list_kn |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\router.py → argparse |
| D2 | INFO | 外部依赖: torch | PASS | :0 | scripts\router.py → torch |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\router.py → utils.MODELS_DIR |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\router.py → utils.find_model_dirs |
| D2 | INFO | 外部依赖: transformers | PASS | :0 | scripts\router.py → transformers.AutoModelForSeque |
| D2 | INFO | 外部依赖: transformers | PASS | :0 | scripts\router.py → transformers.AutoTokenizer |
| D2 | INFO | 外部依赖: torch | PASS | :0 | scripts\router.py → torch |
| D2 | INFO | 外部依赖: langchain_chroma | PASS | :0 | scripts\router.py → langchain_chroma.Chroma |
| D2 | INFO | 外部依赖: rag_core | PASS | :0 | scripts\router.py → rag_core.get_embeddings |
| D2 | INFO | 外部依赖: langchain_text_splitters | PASS | :0 | scripts\text_splitter.py → langchain_text_splitter |
| D2 | INFO | 外部依赖: langchain_core | PASS | :0 | scripts\text_splitter.py → langchain_core.document |
| D2 | INFO | 外部依赖: langchain_text_splitters | PASS | :0 | scripts\text_splitter.py → langchain_text_splitter |
| D2 | INFO | 外部依赖: langchain_core | PASS | :0 | scripts\text_splitter.py → langchain_core.document |
| D2 | INFO | 外部依赖: langchain_text_splitters | PASS | :0 | scripts\text_splitter.py → langchain_text_splitter |
| D2 | INFO | 外部依赖: langchain_core | PASS | :0 | scripts\text_splitter.py → langchain_core.document |
| D2 | INFO | 外部依赖: langchain_core | PASS | :0 | scripts\text_splitter.py → langchain_core.document |
| D2 | INFO | 外部依赖: langchain_core | PASS | :0 | scripts\text_splitter.py → langchain_core.document |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\text_splitter.py → argparse |
| D2 | INFO | 外部依赖: nltk | PASS | :0 | scripts\text_splitter.py → nltk |
| D2 | INFO | 外部依赖: langchain_experimental | PASS | :0 | scripts\text_splitter.py → langchain_experimental. |
| D2 | INFO | 外部依赖: langchain_huggingface | PASS | :0 | scripts\text_splitter.py → langchain_huggingface.H |
| D2 | INFO | 外部依赖: langchain_text_splitters | PASS | :0 | scripts\text_splitter.py → langchain_text_splitter |
| D2 | INFO | 外部依赖: langchain_text_splitters | PASS | :0 | scripts\text_splitter.py → langchain_text_splitter |
| D2 | INFO | 外部依赖: langchain_text_splitters | PASS | :0 | scripts\text_splitter.py → langchain_text_splitter |
| D2 | INFO | 外部依赖: langchain_text_splitters | PASS | :0 | scripts\text_splitter.py → langchain_text_splitter |
| D2 | INFO | 外部依赖: langchain_experimental | PASS | :0 | scripts\text_splitter.py → langchain_experimental. |
| D2 | INFO | 外部依赖: langchain_huggingface | PASS | :0 | scripts\text_splitter.py → langchain_huggingface.H |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\utils.py → time |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\utils.py → threading |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\utils.py → threading |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\utils.py → threading |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\utils.py → threading |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\embedding_model_manager.py:457 | 7 个删除操作分布于不同文件 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:520 | print(json.dumps(models, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:523 | print("未下载任何嵌入模型") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:532 | print(json.dumps(models, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:538 | print("未下载任何 rerank/路由模型") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:561 | print("  建议: 检查网络连接或尝试其他模型") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:563 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:567 | print("\n推荐嵌入模型:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:568 | print("-" * 70) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:570 | print("-" * 70) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:573 | print("-" * 70) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:574 | print("0) 自定义模型 ID") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:585 | print("无效选择") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:595 | print("取消操作") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:598 | print("\n推荐 rerank/路由模型:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:599 | print("-" * 80) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:601 | print("-" * 80) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:604 | print("-" * 80) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:605 | print("0) 自定义模型 ID") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:616 | print("无效选择") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\embedding_model_manager.py:626 | print("取消操作") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\knowledge_base_manager.py:336 | print(json.dumps(kbs, ensure_ascii=False, indent=2 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\knowledge_base_manager.py:345 | print(json.dumps(stats, ensure_ascii=False, indent |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\knowledge_base_manager.py:347 | print("知识库统计:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\knowledge_base_manager.py:382 | print(json.dumps(output, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\prompt_manager.py:96 | print(load_template()) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\prompt_manager.py:111 | print("[OK] 已重置为默认模板") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\prompt_manager.py:115 | print(t) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\prompt_manager.py:132 | print("[OK] 模板包含所有必需占位符") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:260 | print(line, end="", flush=True) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:348 | print("  检查 pip 版本...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:356 | print("    pip 版本已更新") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:364 | print(" (分步策略: 先 install core deps...)") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:379 | print(" OK") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:388 | print("\n  验证安装结果...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:429 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:430 | print("  本地 RAG 环境检测") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:431 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:459 | print("\n" + "=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:527 | print(json.dumps(report, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_env_setup.py:531 | print("\n[dry-run] 检测完成，跳过安装") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:247 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:248 | print("  [阶段 2/6] 环境检测与修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:249 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:268 | print("\n" + "=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:269 | print("  [阶段 3/6] 模型下载") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:270 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:317 | print("\n" + "=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:318 | print("  [阶段 4/6] 知识库创建") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:319 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:339 | print("\n" + "=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:340 | print("  [阶段 5/6] 配置写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:341 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:354 | print("  [OK] 配置已写入 data/config/rag_config.json") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:360 | print("\n" + "=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:361 | print("  [阶段 6/6] 验证") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:362 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:386 | print("  [OK] 32 参数完整") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:404 | print("  [OK] 模型就绪") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:449 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:450 | print("  [阶段 1/6] 参数采集") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:451 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:487 | print("\n" + "=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:489 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:517 | print(json.dumps(CONFIG_SCHEMA, ensure_ascii=False |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:524 | print(json.dumps({ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:532 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_setup_orchestrator.py:533 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:37 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:58 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:76 | print(json.dumps(output, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:90 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:92 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:93 | print("检索到的上下文:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:94 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:95 | print(result["context"]) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:96 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:97 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:98 | print("完整的 Prompt（已填充）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:99 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:100 | print(result["prompt"]) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:102 | print("知识库中未找到相关信息。") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:117 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:119 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:120 | print("检索到的上下文:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:121 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:122 | print(result["context"]) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:124 | print("知识库中未找到相关信息。") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:129 | print(json.dumps({"error": msg, "success": False}, |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:182 | print(json.dumps(output, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_skill.py:193 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:126 | print(""" |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:169 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:170 | print("  local-rag-builder 独立模式") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:171 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:177 | print("  输入 /llm-help 查看外部 LLM 接入指南") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:179 | print("  [i] LLM 已就绪") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:187 | print("  请先运行: python scripts/embedding_model_mana |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:192 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:200 | print("\n退出。") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:211 | print("退出。") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:215 | print(HELP_TEXT) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:225 | print("请输入新模板（输入 END 单独一行结束）：") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:240 | print("[!] 模板为空，未保存") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:242 | print("[OK] 已重置为默认模板") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:244 | print("用法: /prompt show|set|reset") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:267 | print("用法: /kb list|create <name>|use <name>|delet |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:272 | print(json.dumps(load_config(), ensure_ascii=False |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:297 | print("用法: /config show|set <key> <value>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:310 | print("[!] 嵌入模型未加载，请先通过 /model 配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:313 | print("[!] LLM 未连接。输入 /llm-help 查看接入指南，或 /verify-l |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:317 | print("  思考中...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:367 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_standalone.py:385 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\rag_web_ui.py:1439 | print("\n服务器已停止") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\reranker.py:310 | print("当前排序规则:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\reranker.py:315 | print("  （未配置）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\reranker.py:335 | print(json.dumps(output, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\router.py:322 | print(json.dumps(sigs, ensure_ascii=False, indent= |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\router.py:330 | print("[OK] 所有 KB 签名已重建") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\router.py:341 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:673 | print("可用主策略:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:674 | print("-" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:678 | print("\n可用守卫（多选，--guard mermaid,code,math,table,h |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:679 | print("-" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:690 | print("\n可用后处理（--secondary）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:691 | print("-" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:700 | print("\n注意：headers/semantic 主策略的子切会继承 h1/h2/h3/so |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:719 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\text_splitter.py:738 | print(json.dumps({"total_chunks": len(chunks), "ch |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\utils.py:73 | print(line, end="", flush=True) |
| D5 | INFO | 发现 11 个验证函数 | PASS | :0 | _check_integrity, verify_model, check_model_downlo |
| D5 | INFO | 发现 1 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\config | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_config_path() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: load_config() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: reset_config() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 模块可加载: scripts\embedding_model | PASS | :0 |  |
| D5 | INFO | 函数可运行: list_downloaded_models( | PASS | :0 | 返回值类型: list |
| D5 | INFO | 模块可加载: scripts\knowledge_base_ | PASS | :0 |  |
| D5 | INFO | 函数可运行: list_knowledge_bases() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: reset_classify_rules() | PASS | :0 | 返回值类型: tuple |
| D5 | INFO | 函数可运行: get_kb_stats() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 模块可加载: scripts\prompt_manager | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_template_path() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: load_template() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: reset_template() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: get_default_template() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: list_saved_templates() | PASS | :0 | 返回值类型: list |
| D5 | INFO | 模块可加载: scripts\rag_env_setup | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_python_path() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: get_pip_cache_dir() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: find_stale_pip_locks() | PASS | :0 | 返回值类型: list |
| D5 | INFO | 函数可运行: check_python_version() | PASS | :0 | 返回值类型: tuple |
| D5 | INFO | 函数可运行: check_pip() | PASS | :0 | 返回值类型: bool |
| D5 | INFO | 函数可运行: list_installed() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: check_torch_gpu() | PASS | :0 | 返回值类型: tuple |
| D5 | INFO | 函数可运行: run_full_check() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 模块可加载: scripts\rag_setup_orche | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\rag_standalone | PASS | :0 |  |
| D5 | INFO | 函数可运行: verify_llm_connection() | PASS | :0 | 返回值类型: tuple |
| D5 | INFO | 函数可运行: print_llm_help() | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 函数运行失败: run_interactive | FAIL | scripts\rag_standalone.py:164 | 调用时抛出: No module named 'langchain_huggingface' |
| D5 | INFO | 模块可加载: scripts\rag_web_ui | PASS | :0 |  |
| D5 | INFO | 函数可运行: list_templates() | PASS | :0 | 返回值类型: list |
| D5 | INFO | 函数可运行: generate_html() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 模块可加载: scripts\router | PASS | :0 |  |
| D5 | INFO | 函数可运行: list_kb_signatures() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: rebuild_all_signatures( | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 模块可加载: scripts\text_splitter | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_all_strategies_info | PASS | :0 | 返回值类型: list |
| D5 | INFO | 函数可运行: get_all_guards_info() | PASS | :0 | 返回值类型: list |
| D5 | INFO | 模块可加载: scripts\utils | PASS | :0 |  |
| D5 | INFO | 函数可运行: get_python_path() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: check_python_version() | PASS | :0 | 返回值类型: tuple |
| D5 | INFO | 函数可运行: list_installed_packages | PASS | :0 | 返回值类型: dict |
| D6 | INFO | 缺少边界说明 | PASS | scripts\config.py:97 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\config.py:106 | get_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\config.py:115 | update_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\embedding_model_manager.py:134 | _is_model_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\embedding_model_manager.py:204 | _download_with_hf_mirror() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\embedding_model_manager.py:242 | _download_with_hf_direct() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\embedding_model_manager.py:404 | verify_model() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\embedding_model_manager.py:448 | remove_model() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\embedding_model_manager.py:491 | check_model_downloaded() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\knowledge_base_manager.py:27 | _save_index() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\knowledge_base_manager.py:35 | _save_rules() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\knowledge_base_manager.py:86 | delete_knowledge_base() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\knowledge_base_manager.py:104 | get_kb_vectorstore() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\knowledge_base_manager.py:198 | set_classify_rule() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\knowledge_base_manager.py:216 | remove_classify_rule() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\knowledge_base_manager.py:272 | load_documents_from_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\knowledge_base_manager.py:295 | load_documents_from_directory() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\prompt_manager.py:42 | save_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\prompt_manager.py:64 | build_prompt() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\rag_env_setup.py:218 | _pip_run() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\rag_setup_orchestrator.py:221 | build_full_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\rag_setup_orchestrator.py:424 | setup_rag() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\rag_setup_orchestrator.py:122 | _validate() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\rag_web_ui.py:59 | save_template_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\rag_web_ui.py:84 | delete_template_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\rag_web_ui.py:1429 | start_server() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\rag_web_ui.py:1425 | log_message() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\router.py:156 | broadcast_route() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\router.py:278 | update_kb_signature() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\router.py:109 | score() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:57 | register_strategy() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:62 | register_guard() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:67 | get_strategy_config_schema() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:89 | filter_inheritable_meta() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:531 | split_with_mermaid_preserve() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:45 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:117 | restore() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:123 | restore_chunks() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:178 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:186 | add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:191 | apply() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\text_splitter.py:198 | restore() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\utils.py:46 | run_command() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\utils.py:213 | safe_json_load() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\utils.py:224 | find_model_dirs() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\rag_setup_orchestrator.py:0 | scripts\rag_setup_orchestrator.py: 1 个 except / 53 |

### S4 执行忠实度
- 总噪声条目: 21
- 铁律坚守: 21 (100%)
- 正向权重: 0.0, 反向权重: 0.0
- 正向完成率: 0%, 反向坚守率: 100%
- 综合评分: 60% （等级: N/A）
