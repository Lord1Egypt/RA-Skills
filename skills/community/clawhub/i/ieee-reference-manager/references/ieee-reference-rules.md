# IEEE 参考文献格式规范详细手册

> 来源：[IEEE Reference Guide](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf)、[IEEEtran BibTeX HOWTO](https://www.michaelshell.org/tex/ieeetran/bibtex/)

## 一、条目类型与必需字段

### @article（期刊论文）
```bibtex
@article{key,
  author  = {Last1, First1 and Last2, First2},
  title   = {Paper Title},
  journal = IEEE_J_WCOM,          % 必须用 IEEE 宏
  year    = {2024},
  month   = mar,                   % 小写三字母缩写，不加花括号
  volume  = {23},
  number  = {3},
  pages   = {1728--1741},          % 双连字符
  doi     = {10.1109/TWC.xxx}
}
```

### @inproceedings（会议论文）
```bibtex
@inproceedings{key,
  author    = {Last1, First1 and Last2, First2},
  title     = {Paper Title},
  booktitle = {2024 IEEE International Conference on Communications (ICC)},
  year      = {2024},
  month     = jun,
  pages     = {100--105},
  doi       = {10.1109/ICC.xxx}
}
```

### Early Access 文章
```bibtex
@article{key,
  author  = {Last1, First1},
  title   = {Paper Title},
  journal = IEEE_J_WCOM,
  year    = {2025},
  note    = {early access},        % 关键标记
  doi     = {10.1109/TWC.xxx}      % 必须保留
  % 不写 volume, number, pages
}
```

### @book（书籍）
```bibtex
% 作者编写的书籍
@book{key,
  author    = {Last1, First1 and Last2, First2},
  title     = {Book Title},
  publisher = {Publisher Name},
  address   = {City, State/Country},
  year      = {2020}
}

% 编辑主编的书籍
@book{key,
  editor    = {Last1, First1 and Last2, First2},
  title     = {Edited Book Title},
  publisher = {Publisher Name},
  address   = {City, State/Country},
  year      = {2020}
}

% 含版次和丛书信息
@book{key,
  author    = {Last1, First1},
  title     = {Book Title},
  edition   = {Second},
  series    = {Series Name},
  volume    = {5},
  publisher = {Springer-Verlag},
  address   = {Berlin, Germany},
  year      = {2020}
}
```

### @incollection（书籍章节）
```bibtex
@incollection{key,
  author    = {Last1, First1},
  title     = {Chapter Title},
  editor    = {Editor Last, Editor First},
  booktitle = {Book Title},
  publisher = {Publisher Name},
  address   = {City, State/Country},
  year      = {2020},
  chapter   = {3},
  pages     = {45--78}
}
```

### @techreport（技术报告）
```bibtex
@techreport{key,
  author      = {Last1, First1 and Last2, First2},
  title       = {Report Title},
  institution = {Institution Name},
  address     = {City, State/Country},
  number      = {TR-2024-001},
  month       = aug,
  year        = {2024}
}
% type 字段可覆盖默认的 "Tech. Rep." 标识
% 如 type = {CMPSCI Tech. Rep.}
```

### @standard（技术标准：IEEE / 3GPP / ISO 等）
```bibtex
% IEEE 标准
@standard{key,
  title        = {Wireless {LAN} Medium Access Control {(MAC)} and
                  Physical Layer {(PHY)} Specification},
  organization = {IEEE},
  address      = {Piscataway, NJ},
  number       = {802.11},
  year         = {2020}
}

% 3GPP 标准
@standard{key,
  title        = {Study on New Radio ({NR}) Access Technology},
  organization = {3rd Generation Partnership Project ({3GPP})},
  type         = {TR},                   % 或 TS
  number       = {38.912 V15.0.0},
  month        = jun,
  year         = {2018}
}

% ISO 标准
@standard{key,
  title        = {Information Technology---Open Systems Interconnection},
  organization = {ISO/IEC},
  number       = {7498-1},
  year         = {1994}
}
```
> **注意**：`@standard` 是 IEEEtran.bst 扩展类型，非标准 BibTeX。若使用其他 .bst 可用 `@misc` 替代。

### @electronic（在线资源 / 网页）
```bibtex
% 有作者的在线资源
@electronic{key,
  author       = {Last1, First1},
  title        = {Webpage or Resource Title},
  url          = {https://example.com/resource},
  year         = {2024}
}

% 带来源描述（howpublished 描述资源形式，如 mailing list、Internet draft 等）
@electronic{key,
  author       = {Last1, First1},
  title        = {Resource Title},
  howpublished = {Internet draft},           % 描述资源类别，非 [Online]
  url          = {https://example.com/draft},
  year         = {2024}
}

% 无个人作者的网站（用 key 字段提供排序依据）
@electronic{key,
  title        = {The {IEEE} Website},
  url          = {https://www.ieee.org/},
  year         = {2024},
  key          = {IEEE}
}
```
> **IEEEtran.bst 渲染规则**：`@electronic` 条目会自动生成 `[Online]. Available: URL` 格式输出。
> **不要**手动写 `howpublished = {[Online]}`，否则会导致重复输出。`howpublished` 应用于描述来源类别（如 `Internet draft`、`end2end-interest mailing list`）。
>
> **访问日期**：IEEE 要求在线资源注明访问日期。可通过 `note` 字段添加：
> ```bibtex
> note = {Accessed: Mar. 10, 2026}
> ```
> 对于频繁更新的网页建议加上；对于稳定的在线资源（如官方文档）可省略。
>
> `@electronic` 是 IEEEtran.bst 扩展类型。若使用其他 .bst，可用 `@misc` + `howpublished = {\url{...}}` 替代。

### @misc（arXiv 预印本 / 待发表 / 其他）

#### arXiv 预印本
```bibtex
@misc{key,
  author       = {Last1, First1 and Last2, First2},
  title        = {Paper Title},
  howpublished = {arXiv preprint arXiv:2401.12345},
  year         = {2024}
}
```
> **IEEE 官方要求**：若论文已被期刊 Early Access 或正式发表，应引用出版版本而非 arXiv 版本。

#### 待发表（To Be Published）
```bibtex
@misc{key,
  author       = {Last1, First1},
  title        = {Paper Title},
  howpublished = IEEE_J_WCOM,
  note         = {to be published},
  year         = {2025}
}
```

#### RFC 文档
```bibtex
@misc{key,
  author       = {Last1, First1 and Last2, First2},
  title        = {{RFC} Title},
  howpublished = {RFC 9293},
  month        = aug,
  year         = {2022}
}
```

#### 白皮书 / 数据手册
```bibtex
@misc{key,
  title        = {White Paper Title},
  howpublished = {White Paper},
  organization = {Company Name},
  year         = {2024}
}
```

### @phdthesis / @mastersthesis（学位论文）
```bibtex
@phdthesis{key,
  author  = {Last1, First1},
  title   = {Dissertation Title},
  school  = {University Name},
  address = {City, State/Country},
  year    = {2023}
}

@mastersthesis{key,
  author  = {Last1, First1},
  title   = {Thesis Title},
  school  = {University Name},
  address = {City, State/Country},
  year    = {2023}
}
% type 字段可覆盖默认标识，如 type = {M. Eng. thesis}
```

### @patent（专利）
```bibtex
@patent{key,
  author      = {Last1, First1 and Last2, First2},
  title       = {Patent Title},
  nationality = {United States},
  number      = {1234567},
  month       = sep,
  year        = {2023}
}
```
> `@patent` 是 IEEEtran.bst 扩展类型。支持 `assignee`、`dayfiled`、`monthfiled`、`yearfiled` 等字段。

---

## 二、IEEE 期刊宏对照表（常用）

| 宏名 | 全名 | 缩写 |
|------|------|------|
| `IEEE_J_WCOM` | IEEE Trans. Wireless Commun. | TWC |
| `IEEE_J_VT` | IEEE Trans. Veh. Technol. | TVT |
| `IEEE_J_JSAC` | IEEE J. Sel. Areas Commun. | JSAC |
| `IEEE_J_COM` | IEEE Trans. Commun. | TCOM |
| `IEEE_J_MC` | IEEE Trans. Mobile Comput. | TMC |
| `IEEE_J_IOT` | IEEE Internet Things J. | IoT-J |
| `IEEE_J_NET` | IEEE/ACM Trans. Netw. | ToN |
| `IEEE_J_AC` | IEEE Trans. Autom. Control | TAC |
| `IEEE_J_SP` | IEEE Trans. Signal Process. | TSP |
| `IEEE_J_IT` | IEEE Trans. Inf. Theory | TIT |
| `IEEE_J_ITS` | IEEE Trans. Intell. Transp. Syst. | TITS |
| `IEEE_J_IINF` | IEEE Trans. Ind. Informat. | TII |
| `IEEE_J_NSE` | IEEE Trans. Netw. Sci. Eng. | TNSE |
| `IEEE_J_COML` | IEEE Commun. Lett. | CL |
| `IEEE_O_ACC` | IEEE Access | Access |
| `IEEE_O_CSTO` | IEEE Commun. Surv. Tutorials | COMST |

完整列表见 IEEEabrv.bib。

## 三、BSTcontrol 配置

```bibtex
@ieeetranbstctl{IEEEexample:BSTcontrol,
  ctluse_forced_etal        = {yes},  % 启用 et al. 截断
  ctlmax_names_forced_et_al = {6},    % 超过 6 位时触发
  ctlnames_show_etal        = {1}     % 显示 1 位作者 + et al.
}
```

在 .tex 中必须调用：
```latex
\bstctlcite{IEEEexample:BSTcontrol}  % 放在第一个 \cite 之前
```

## 四、\cite 命令规范

| 场景 | 正确写法 | 错误写法 |
|------|---------|---------|
| 单引用 | `\cite{key}` | - |
| 多引用 | `\cite{key1, key2, key3}` | `\cite{key1}, \cite{key2}` |
| 文中提及 | `the authors in \cite{key}` | `the authors in [1]` |
| 句末引用 | `...method~\cite{key}.` | `...method \cite{key} .` |

注意：`~` 不换行空格保证引用不与前文断行。

## 五、常见错误与修复

### 5.1 月份格式
```bibtex
% 正确（IEEEtran.bst 自动格式化）
month = mar,
month = {Mar.},

% 错误
month = {March},
month = {3},
```

### 5.2 页码格式
```bibtex
% 正确
pages = {100--110},

% 错误
pages = {100-110},    % 单连字符
pages = {1--1},       % Early Access 占位符
```

### 5.3 标题大小写保护
BibTeX 默认将标题转换为 sentence case。需要保持大写的专有名词用 `{{}}` 保护：
```bibtex
title = {Deep {{Reinforcement Learning}} for {{UAV}} Networks}
```

**需要保护的常见情况：**
- 缩写词：`{{UAV}}`、`{{MIMO}}`、`{{NOMA}}`、`{{IoT}}`、`{{QoS}}`、`{{DRL}}`
- 专有名词/协议：`{{Lyapunov}}`、`{{Markov}}`、`{{Shannon}}`、`{{TCP}}`、`{{LTE}}`
- 算法/框架名：`{{MAPPO}}`、`{{PPO}}`、`{{Transformer}}`、`{{ResNet}}`
- 标准组织/系统：`{{IEEE}}`、`{{3GPP}}`、`{{OFDM}}`、`{{5G}}`、`{{NR}}`
- 注意：`booktitle`（会议名）不受此影响，无需保护

### 5.4 非 IEEE 期刊
对于非 IEEE 期刊（如 Springer, Elsevier），直接写缩写名：
```bibtex
journal = {J. Supercomput.},
```

## 六、DOI 验证方法

### 通过 DOI 解析器
URL 格式：`https://doi.org/10.1109/TWC.2024.xxxx`
- 正常：重定向到论文页面
- 异常：404 或无法解析

### 通过 IEEE Xplore 搜索
- 搜索标题或 DOI
- 比对作者、年份、期刊、页码

### 批量验证策略
1. 提取所有 DOI
2. 格式检查（应以 `10.` 开头）
3. 按优先级验证（Early Access > 近年 > 早期）
