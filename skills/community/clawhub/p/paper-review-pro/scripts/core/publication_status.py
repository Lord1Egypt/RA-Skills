#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
论文发表状态与 CCF 评级查询模块

功能：
1. 查询论文是否已发表在会议或期刊
2. 获取 CCF（中国计算机学会）评级
3. 未发表的论文标记为 preprint
4. 将发表状态和评级纳入评分体系

CCF 评级说明（第七版，2026 年 3 月更新）：
- A 类：顶级会议/期刊，影响力极高
- B 类：优秀会议/期刊，影响力高
- C 类：良好会议/期刊，有一定影响力

数据来源：中国计算机学会推荐国际学术会议和期刊目录（第七版，2026 年 3 月）
"""

import os
import re
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, List, Tuple, Set


# =========================
# CCF 评级数据库（第七版，2026 年 3 月）
# =========================
# 格式：{简称/关键词：评级}
# 包含会议/期刊的简称和全称关键词，用于模糊匹配

# CCF-A 类会议
CCF_A_CONFERENCES = {
    # 计算机体系结构/并行与分布计算/存储系统
    "ppopp": "ACM SIGPLAN Symposium on Principles & Practice of Parallel Programming",
    "fast": "USENIX Conference on File and Storage Technologies",
    "dac": "Design Automation Conference",
    "hpca": "IEEE International Symposium on High Performance Computer Architecture",
    "micro": "IEEE/ACM International Symposium on Microarchitecture",
    "sc": "International Conference for High Performance Computing, Networking, Storage, and Analysis",
    "asplos": "International Conference on Architectural Support for Programming Languages and Operating Systems",
    "isca": "International Symposium on Computer Architecture",
    "usenix atc": "USENIX Annual Technical Conference",
    "acm sigops atc": "ACM SIGOPS Annual Technical Conference",
    "eurosys": "European Conference on Computer Systems",
    "hpdc": "The International ACM Symposium on High-Performance Parallel and Distributed Computing",
    # 计算机网络
    "sigcomm": "ACM International Conference on Applications, Technologies, Architectures, and Protocols for Computer Communication",
    "mobicom": "ACM International Conference on Mobile Computing and Networking",
    "infocom": "IEEE International Conference on Computer Communications",
    "nsdi": "Symposium on Network System Design and Implementation",
    # 网络与信息安全
    "ccs": "ACM Conference on Computer and Communications Security",
    "acm conference on computer and communications security": "ACM Conference on Computer and Communications Security",
    "eurocrypt": "International Conference on the Theory and Applications of Cryptographic Techniques",
    "s&p": "IEEE Symposium on Security and Privacy",
    "oakland": "IEEE Symposium on Security and Privacy",
    "crypto": "International Cryptology Conference",
    "usenix security": "USENIX Security Symposium",
    "ndss": "Network and Distributed System Security Symposium",
    # 软件工程/系统软件/程序设计语言
    "pldi": "ACM SIGPLAN Conference on Programming Language Design and Implementation",
    "popl": "ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages",
    "fse": "ACM International Conference on the Foundations of Software Engineering",
    "sigsoft": "ACM International Conference on the Foundations of Software Engineering",
    "sosp": "ACM Symposium on Operating Systems Principles",
    "oopsla": "Conference on Object-Oriented Programming Systems, Languages, and Applications",
    "ase": "International Conference on Automated Software Engineering",
    "icse": "International Conference on Software Engineering",
    "issta": "International Symposium on Software Testing and Analysis",
    "osdi": "USENIX Symposium on Operating Systems Design and Implementation",
    "fm": "International Symposium on Formal Methods",
    # 数据库/数据挖掘/内容检索
    "sigmod": "ACM International Conference on Management of Data",
    "vldb": "International Conference on Very Large Data Bases",
    "icde": "IEEE International Conference on Data Engineering",
    "pods": "ACM SIGMOD-SIGACT-SIGAI Symposium on Principles of Database Systems",
    "kdd": "ACM SIGKDD International Conference on Knowledge Discovery and Data Mining",
    "www": "The Web Conference",
    "sigir": "ACM International Conference on Research and Development in Information Retrieval",
    "cikm": "ACM International Conference on Information and Knowledge Management",
    "recsys": "ACM Conference on Recommender Systems",
    # 人工智能
    "neurips": "Conference on Neural Information Processing Systems",
    "nips": "Conference on Neural Information Processing Systems",
    "icml": "International Conference on Machine Learning",
    "iclr": "International Conference on Learning Representations",
    "aaai": "AAAI Conference on Artificial Intelligence",
    "ijcai": "International Joint Conference on Artificial Intelligence",
    "colt": "Annual Conference on Learning Theory",
    "uai": "Conference on Uncertainty in Artificial Intelligence",
    "acl": "Annual Meeting of the Association for Computational Linguistics",
    "emnlp": "Conference on Empirical Methods in Natural Language Processing",
    "naacl": "Annual Conference of the North American Chapter of the Association for Computational Linguistics",
    "coling": "International Conference on Computational Linguistics",
    "cvpr": "IEEE/CVF Conference on Computer Vision and Pattern Recognition",
    "iccv": "IEEE/CVF International Conference on Computer Vision",
    "eccv": "European Conference on Computer Vision",
    "acm mm": "ACM International Conference on Multimedia",
    "nlpcc": "CCF International Conference on Natural Language Processing and Chinese Computing",
    # 人机交互
    "chi": "ACM Conference on Human Factors in Computing Systems",
    "ubicomp": "ACM International Joint Conference on Pervasive and Ubiquitous Computing",
    "cscw": "ACM Conference on Computer-Supported Cooperative Work and Social Computing",
    # 图形学
    "siggraph": "ACM SIGGRAPH Annual Conference",
    "siggraph asia": "ACM SIGGRAPH Asia",
    # 系统/网络
    "sosp": "ACM Symposium on Operating Systems Principles",
    "osdi": "USENIX Symposium on Operating Systems Design and Implementation",
    "nsdi": "Symposium on Network System Design and Implementation",
}

# CCF-B 类会议
CCF_B_CONFERENCES = {
    # 计算机体系结构/并行与分布计算/存储系统
    "socc": "ACM Symposium on Cloud Computing",
    "spaa": "ACM Symposium on Parallelism in Algorithms and Architectures",
    "podc": "ACM Symposium on Principles of Distributed Computing",
    "fpga": "ACM/SIGDA International Symposium on Field-Programmable Gate Arrays",
    "cgo": "The International Symposium on Code Generation and Optimization",
    "date": "Design, Automation & Test in Europe",
    "hot chips": "Hot Chips: A Symposium on High Performance Chips",
    "cluster": "IEEE International Conference on Cluster Computing",
    "iccd": "International Conference on Computer Design",
    "iccad": "International Conference on Computer-Aided Design",
    "icdcs": "IEEE International Conference on Distributed Computing Systems",
    "codes+isss": "International Conference on Hardware/Software Co-design and System Synthesis",
    "hipeac": "International Conference on High Performance and Embedded Architectures and Compilers",
    "sigmetrics": "International Conference on Measurement and Modeling of Computer Systems",
    "pact": "International Conference on Parallel Architectures and Compilation Techniques",
    "icpp": "International Conference on Parallel Processing",
    "ics": "International Conference on Supercomputing",
    "vee": "International Conference on Virtual Execution Environments",
    "ipdps": "IEEE International Parallel & Distributed Processing Symposium",
    "performance": "International Symposium on Computer Performance, Modeling, Measurements and Evaluation",
    "itc": "International Test Conference",
    "lisa": "Large Installation System Administration Conference",
    "msst": "Mass Storage Systems and Technologies",
    "rtas": "IEEE Real-Time and Embedded Technology and Applications Symposium",
    "euro-par": "European Conference on Parallel and Distributed Computing",
    "iscas": "IEEE International Symposium on Circuits and Systems",
    # 计算机网络
    "sensys": "ACM Conference on Embedded Networked Sensor Systems",
    "conext": "ACM International Conference on Emerging Networking Experiments and Technologies",
    "secon": "IEEE International Conference on Sensing, Communication, and Networking",
    "ipsn": "International Conference on Information Processing in Sensor Networks",
    "mobisys": "ACM International Conference on Mobile Systems, Applications, and Services",
    "icnp": "IEEE International Conference on Network Protocols",
    "mobihoc": "International Symposium on Theory, Algorithmic Foundations, and Protocol Design for Mobile Networks and Mobile Computing",
    "nossdav": "International Workshop on Network and Operating System Support for Digital Audio and Video",
    "iwqos": "IEEE/ACM International Workshop on Quality of Service",
    "imc": "ACM Internet Measurement Conference",
    # 网络与信息安全
    "acsac": "Annual Computer Security Applications Conference",
    "asiacrypt": "Annual International Conference on the Theory and Application of Cryptology and Information Security",
    "esorics": "European Symposium on Research in Computer Security",
    "fse": "Fast Software Encryption",
    "csfw": "IEEE Computer Security Foundations Workshop",
    "srds": "IEEE International Symposium on Reliable Distributed Systems",
    "ches": "International Conference on Cryptographic Hardware and Embedded Systems",
    "dsn": "International Conference on Dependable Systems and Networks",
    "raid": "International Symposium on Recent Advances in Intrusion Detection",
    "pkc": "International Workshop on Practice and Theory in Public Key Cryptography",
    "tcc": "Theory of Cryptography Conference",
    # 软件工程/系统软件/程序设计语言
    "ecoop": "European Conference on Object-Oriented Programming",
    "etaps": "European Joint Conferences on Theory and Practice of Software",
    "icpc": "IEEE International Conference on Program Comprehension",
    "re": "IEEE International Requirements Engineering Conference",
    "caise": "International Conference on Advanced Information Systems Engineering",
    "icfp": "ACM SIGPLAN International Conference on Functional Programming",
    "lctes": "ACM SIGPLAN/SIGBED International Conference on Languages, Compilers and Tools for Embedded Systems",
    "models": "ACM/IEEE International Conference on Model Driven Engineering Languages and Systems",
    "cp": "International Conference on Principles and Practice of Constraint Programming",
    "icsoc": "International Conference on Service Oriented Computing",
    "saner": "IEEE International Conference on Software Analysis, Evolution, and Reengineering",
    "icsme": "International Conference on Software Maintenance and Evolution",
    "vmcai": "International Conference on Verification, Model Checking and Abstract Interpretation",
    "icws": "IEEE International Conference on Web Services",
    "middleware": "International Middleware Conference",
    "sas": "International Static Analysis Symposium",
    "esem": "International Symposium on Empirical Software Engineering and Measurement",
    "issre": "IEEE International Symposium on Software Reliability Engineering",
    "hotos": "USENIX Workshop on Hot Topics in Operating Systems",
    "cc": "International Conference on Compiler Construction",
    # 数据库/数据挖掘/内容检索
    "icdt": "International Conference on Database Theory",
    "edbt": "International Conference on Extending Database Technology",
    "ssdbm": "International Conference on Scientific and Statistical Database Management",
    "dl": "ACM/IEEE Joint Conference on Digital Libraries",
    "ecir": "European Conference on Information Retrieval",
    "wis": "Web Information Systems Engineering",
    "apweb": "Asia Pacific Web Conference",
    "dasfaa": "Database Systems for Advanced Applications",
    # 人工智能
    "icann": "International Conference on Artificial Neural Networks",
    "iconip": "International Conference on Neural Information Processing",
    "pricai": "Pacific Rim International Conference on Artificial Intelligence",
    "conll": "Conference on Computational Natural Language Learning",
    "semeval": "International Workshop on Semantic Evaluation",
    "wacv": "IEEE Winter Conference on Applications of Computer Vision",
    "bmvc": "British Machine Vision Conference",
    "icip": "IEEE International Conference on Image Processing",
    "accv": "Asian Conference on Computer Vision",
    "psb": "Pacific Symposium on Biocomputing",
    "ismb": "Intelligent Systems for Molecular Biology",
    # 人机交互
    "iui": "ACM International Conference on Intelligent User Interfaces",
    "group": "ACM International Conference on Supporting Group Work",
    "dis": "ACM Conference on Designing Interactive Systems",
    "uist": "ACM Symposium on User Interface Software and Technology",
    "idc": "ACM International Conference on Interaction Design and Children",
    # 图形学
    "sgi": "Eurographics Symposium on Geometry Processing",
    "egsr": "Eurographics Symposium on Rendering",
    "sca": "ACM/Eurographics Symposium on Computer Animation",
    "eg": "Eurographics",
    "pg": "Pacific Graphics",
}

# CCF-C 类会议
CCF_C_CONFERENCES = {
    # 计算机体系结构/并行与分布计算/存储系统
    "cf": "ACM International Conference on Computing Frontiers",
    "systor": "ACM International Systems and Storage Conference",
    "nocs": "ACM/IEEE International Symposium on Networks-on-Chip",
    "asap": "IEEE International Conference on Application-Specific Systems, Architectures, and Processors",
    "asp-dac": "Asia and South Pacific Design Automation Conference",
    "ets": "IEEE European Test Symposium",
    "fpl": "International Conference on Field-Programmable Logic and Applications",
    "fccm": "IEEE Symposium on Field-Programmable Custom Computing Machines",
    "glsvlsi": "Great Lakes Symposium on VLSI",
    "ats": "IEEE Asian Test Symposium",
    "hpcc": "IEEE International Conference on High Performance Computing and Communications",
    "hipc": "IEEE International Conference on High Performance Computing, Data and Analytics",
    "mascots": "International Symposium on Modeling, Analysis, and Simulation of Computer and Telecommunication Systems",
    "ispa": "IEEE International Symposium on Parallel and Distributed Processing with Applications",
    "ccgrid": "IEEE/ACM International Symposium on Cluster, Cloud and Grid Computing",
    "npc": "IFIP International Conference on Network and Parallel Computing",
    "ica3pp": "International Conference on Algorithms and Architectures for Parallel Processing",
    "cases": "International Conference on Compilers, Architectures, and Synthesis for Embedded Systems",
    "fpt": "International Conference on Field-Programmable Technology",
    "icpads": "International Conference on Parallel and Distributed Systems",
    "islped": "International Symposium on Low Power Electronics and Design",
    "ispd": "International Symposium on Physical Design",
    "hoti": "IEEE Symposium on High-Performance Interconnects",
    "vts": "IEEE VLSI Test Symposium",
    "itc-asia": "International Test Conference in Asia",
    "sec": "ACM/IEEE Symposium on Edge Computing",
    "nas": "International Conference on Networking, Architecture and Storage",
    "hotstorage": "HotStorage",
    "appt": "International Symposium on Advanced Parallel Processing Technology",
    # 计算机网络
    "ancs": "ACM/IEEE Symposium on Architectures for Networking and Communication Systems",
    "apnoms": "Asia-Pacific Network Operations and Management Symposium",
    "forte": "International Conference on Formal Techniques for Distributed Objects, Components, and Systems",
    "lcn": "IEEE Conference on Local Computer Networks",
    "globecom": "IEEE Global Communications Conference",
    "icc": "IEEE International Conference on Communications",
    "icccn": "IEEE International Conference on Computer Communications and Networks",
    "mass": "IEEE International Conference on Mobile Ad hoc and Sensor Systems",
    "p2p": "IEEE International Conference on Peer-to-Peer Computing",
    "ipccc": "IEEE International Performance Computing and Communications Conference",
    "wowmom": "IEEE International Symposium on a World of Wireless, Mobile and Multimedia Networks",
    "iscc": "IEEE Symposium on Computers and Communications",
    "wcnc": "IEEE Wireless Communications and Networking Conference",
    "networking": "IFIP International Conferences on Networking",
    "im": "IFIP/IEEE International Symposium on Integrated Network Management",
    "msn": "International Conference on Mobility, Sensing and Networking",
    "mswim": "International Conference on Modeling, Analysis and Simulation of Wireless and Mobile Systems",
    "wasa": "The International Conference on Wireless Artificial Intelligent Computing Systems and Applications",
    "hotnets": "ACM The Workshop on Hot Topics in Networks",
    "apnet": "Asia-Pacific Workshop on Networking",
    # 网络与信息安全
    "wisec": "ACM Conference on Security and Privacy in Wireless and Mobile Networks",
    "sacmat": "ACM Symposium on Access Control Models and Technologies",
    "drm": "ACM Workshop on Digital Rights Management",
    "ih&mmsec": "ACM Workshop on Information Hiding and Multimedia Security",
    "acns": "International Conference on Applied Cryptography and Network Security",
    "asiaccs": "ACM Asia Conference on Computer and Communications Security",
    "acisp": "Australasia Conference on Information Security and Privacy",
    "ct-rsa": "The Cryptographer's Track at RSA Conference",
    "dimva": "Conference on Detection of Intrusions and Malware & Vulnerability Assessment",
    "dfrws": "Digital Forensic Research Workshop",
    "fc": "Financial Cryptography and Data Security",
    "trustcom": "IEEE International Conference on Trust, Security and Privacy in Computing and Communications",
    "isc": "Information Security Conference",
    "icdf2c": "International Conference on Digital Forensics & Cyber Crime",
    "icics": "International Conference on Information and Communications Security",
    "securecomm": "International Conference on Security and Privacy in Communication Networks",
    "nspw": "New Security Paradigms Workshop",
    "pam": "Passive and Active Measurement Conference",
    "pets": "Privacy Enhancing Technologies Symposium",
    "sac": "Selected Areas in Cryptography",
    "soups": "Symposium On Usable Privacy and Security",
    "hotsec": "USENIX Workshop on Hot Topics in Security",
    "eurosp": "IEEE European Symposium on Security and Privacy",
    "inscrypt": "International Conference on Information Security and Cryptology",
    "codaspy": "Conference on Data and Application Security and Privacy",
    # 软件工程/系统软件/程序设计语言
    "pepm": "ACM SIGPLAN Workshop on Partial Evaluation and Program Manipulation",
    "paste": "ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering",
    "aplas": "Asian Symposium on Programming Languages and Systems",
    "apsec": "Asia-Pacific Software Engineering Conference",
    "ease": "International Conference on Evaluation and Assessment in Software Engineering",
    "iceccs": "International Conference on Engineering of Complex Computer Systems",
    "icst": "IEEE International Conference on Software Testing, Verification and Validation",
    "ispass": "IEEE International Symposium on Performance Analysis of Systems and Software",
    "scam": "IEEE International Working Conference on Source Code Analysis and Manipulation",
    "compsac": "International Computer Software and Applications Conference",
    "icfem": "International Conference on Formal Engineering Methods",
    "scc": "IEEE International Conference on Software Services Engineering",
    "icsp": "International Conference on Software and System Process",
    "seke": "International Conference on Software Engineering and Knowledge Engineering",
    "qrs": "International Conference on Software Quality, Reliability and Security",
    "icsr": "International Conference on Software Reuse",
    "icwe": "International Conference on Web Engineering",
    "spin": "International Symposium on Model Checking of Software",
    "atva": "International Symposium on Automated Technology for Verification and Analysis",
    "lopstr": "International Symposium on Logic-based Program Synthesis and Transformation",
    "tase": "Theoretical Aspects of Software Engineering Conference",
    "msr": "Mining Software Repositories",
    "refsq": "Requirements Engineering: Foundation for Software Quality",
    "wicsa": "Working IEEE/IFIP Conference on Software Architecture",
    "internetware": "Asia-Pacific Symposium on Internetware",
    "rv": "International Conference on Runtime Verification",
    "memocode": "International Conference on Formal Methods and Models for Co-Design",
    # 数据库/数据挖掘/内容检索
    "ssd": "International Symposium on Spatial and Temporal Databases",
    "cidr": "Conference on Innovative Data Systems Research",
    "adbis": "East European Conference on Advances in Databases and Information Systems",
    "flex": "ACM SIGMOD Workshop on Flexible and Scalable Big Data Platform Technologies",
    "smod": "ACM SIGMOD Workshop on Data Management on New Hardware",
    "air": "Workshop on Algorithmic Aspects of Information Retrieval",
    "ictir": "ACM SIGIR International Conference on Theory of Information Retrieval",
    "iiix": "ACM SIGIR Conference on Information Interaction in Context",
    "sac": "ACM Symposium on Applied Computing",
    # 人工智能
    "ijcnn": "International Joint Conference on Neural Networks",
    "icpr": "International Conference on Pattern Recognition",
    "ialp": "International Conference on Asian Language Processing",
    "rocling": "The Conference on Computational Linguistics and Speech Processing",
}

# CCF-A 类期刊
CCF_A_JOURNALS = {
    # 计算机体系结构/并行与分布计算/存储系统
    "tocs": "ACM Transactions on Computer Systems",
    "tos": "ACM Transactions on Storage",
    "tcad": "IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems",
    "tc": "IEEE Transactions on Computers",
    "tpds": "IEEE Transactions on Parallel and Distributed Systems",
    "taco": "ACM Transactions on Architecture and Code Optimization",
    # 计算机网络
    "jsac": "IEEE Journal on Selected Areas in Communications",
    "tmc": "IEEE Transactions on Mobile Computing",
    "ton": "IEEE/ACM Transactions on Networking",
    # 网络与信息安全
    "tdsc": "IEEE Transactions on Dependable and Secure Computing",
    "tifs": "IEEE Transactions on Information Forensics and Security",
    "ieee tifs": "IEEE Transactions on Information Forensics and Security",
    "ieee transactions on information forensics and security": "IEEE Transactions on Information Forensics and Security",
    "journal of cryptology": "Journal of Cryptology",
    # 软件工程/系统软件/程序设计语言
    "toplas": "ACM Transactions on Programming Languages and Systems",
    "tosem": "ACM Transactions on Software Engineering and Methodology",
    "tse": "IEEE Transactions on Software Engineering",
    "tsc": "IEEE Transactions on Services Computing",
    # 数据库/数据挖掘/内容检索
    "tods": "ACM Transactions on Database Systems",
    "tois": "ACM Transactions on Information Systems",
    "tkde": "IEEE Transactions on Knowledge and Data Engineering",
    "vldb j": "The VLDB Journal",
    # 人工智能
    "artificial intelligence": "Artificial Intelligence",
    "ieee tpami": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "tpami": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "jmlr": "Journal of Machine Learning Research",
    "ijcv": "International Journal of Computer Vision",
    "tacl": "Transactions of the Association for Computational Linguistics",
    "computational linguistics": "Computational Linguistics",
    "ieee tip": "IEEE Transactions on Image Processing",
}

# CCF-B 类期刊
CCF_B_JOURNALS = {
    # 计算机体系结构/并行与分布计算/存储系统
    "taas": "ACM Transactions on Autonomous and Adaptive Systems",
    "todaes": "ACM Transactions on Design Automation of Electronic Systems",
    "tecs": "ACM Transactions on Embedded Computing Systems",
    "trets": "ACM Transactions on Reconfigurable Technology and Systems",
    "tvlsi": "IEEE Transactions on Very Large Scale Integration (VLSI) Systems",
    "jpdc": "Journal of Parallel and Distributed Computing",
    "jsa": "Journal of Systems Architecture: Embedded Software Design",
    "pc": "Parallel Computing",
    "pe": "Performance Evaluation: An International Journal",
    "tcc": "IEEE Transactions on Cloud Computing",
    "ieee transactions on multimedia": "IEEE Transactions on Multimedia",
    "ieee tmm": "IEEE Transactions on Multimedia",
    "tmm": "IEEE Transactions on Multimedia",
    # 计算机网络
    "toit": "ACM Transactions on Internet Technology",
    "tomm": "ACM Transactions on Multimedia Computing, Communications and Applications",
    "tosn": "ACM Transactions on Sensor Networks",
    "cn": "Computer Networks",
    "tcom": "IEEE Transactions on Communications",
    "twc": "IEEE Transactions on Wireless Communications",
    # 网络与信息安全
    "tops": "ACM Transactions on Privacy and Security",
    "computers & security": "Computers & Security",
    "dcc": "Designs, Codes and Cryptography",
    "jcs": "Journal of Computer Security",
    "cybersecurity": "Cybersecurity",
    # 软件工程/系统软件/程序设计语言
    "ase": "Automated Software Engineering",
    "ese": "Empirical Software Engineering",
    "iet software": "IET Software",
    "ist": "Information and Software Technology",
    "jfp": "Journal of Functional Programming",
    "jsme": "Journal of Software: Evolution and Process",
    "jss": "Journal of Systems and Software",
    "re": "Requirements Engineering",
    "scp": "Science of Computer Programming",
    "sosym": "Software and Systems Modeling",
    "stvr": "Software Testing, Verification and Reliability",
    "spe": "Software: Practice and Experience",
    # 数据库/数据挖掘/内容检索
    "tkdd": "ACM Transactions on Knowledge Discovery from Data",
    "tweb": "ACM Transactions on the Web",
    "aei": "Advanced Engineering Informatics",
    "dke": "Data & Knowledge Engineering",
    "dmkd": "Data Mining and Knowledge Discovery",
    "is": "Information Systems",
    "jasist": "Journal of the Association for Information Science and Technology",
    "jws": "Journal of Web Semantics",
    # 人工智能
    "ieee tnnls": "IEEE Transactions on Neural Networks and Learning Systems",
    "neural networks": "Neural Networks",
    "machine learning": "Machine Learning",
    "ieee tmm": "IEEE Transactions on Multimedia",
    "tmm": "IEEE Transactions on Multimedia",
    "pattern recognition": "Pattern Recognition",
    "kais": "Knowledge and Information Systems",
    "ieee spl": "IEEE Signal Processing Letters",
    "signal processing": "Signal Processing",
    "mtap": "Multimedia Tools and Applications",
    "acm tallip": "ACM Transactions on Asian and Low-Resource Language Information Processing",
    "ieee taslp": "IEEE/ACM Transactions on Audio, Speech, and Language Processing",
}

# CCF-C 类期刊
CCF_C_JOURNALS = {
    # 计算机体系结构/并行与分布计算/存储系统
    "jetc": "ACM Journal on Emerging Technologies in Computing Systems",
    "cpe": "Concurrency and Computation: Practice and Experience",
    "dc": "Distributed Computing",
    "fgcs": "Future Generation Computer Systems",
    "integration": "Integration, the VLSI Journal",
    "jetta": "Journal of Electronic Testing - Theory and Applications",
    "jgc": "Journal of Grid Computing",
    "rts": "Real-Time Systems",
    "tjsc": "The Journal of Supercomputing",
    "tcas-i": "IEEE Transactions on Circuits and Systems I: Regular Papers",
    "ccf-thpc": "CCF Transactions on High Performance Computing",
    "tsusc": "IEEE Transactions on Sustainable Computing",
    "expert systems with applications": "Expert Systems with Applications",
    "eswa": "Expert Systems with Applications",
    # 计算机网络
    "ad hoc networks": "Ad Hoc Networks",
    "cc": "Computer Communications",
    "tnsm": "IEEE Transactions on Network and Service Management",
    "iet communications": "IET Communications",
    "jnca": "Journal of Network and Computer Applications",
    "monet": "Mobile Networks and Applications",
    "networks": "Networks",
    "ppna": "Peer-to-Peer Networking and Applications",
    "wcmc": "Wireless Communications and Mobile Computing",
    "wireless networks": "Wireless Networks",
    "iot": "IEEE Internet of Things Journal",
    "tiot": "ACM Transactions on Internet of Things",
    # 网络与信息安全
    "clsr": "Computer Law & Security Review",
    "eurasip jis": "EURASIP Journal on Information Security",
    "iet information security": "IET Information Security",
    "imcs": "Information and Computer Security",
    "ijics": "International Journal of Information and Computer Security",
    "ijisp": "International Journal of Information Security and Privacy",
    "jisa": "Journal of Information Security and Applications",
    "scn": "Security and Communication Networks",
    "hcc": "High-Confidence Computing",
    # 软件工程/系统软件/程序设计语言
    "cl": "Computer Languages, Systems and Structures",
    "ijseke": "International Journal of Software Engineering and Knowledge Engineering",
    "sttt": "International Journal on Software Tools for Technology Transfer",
    "jlamp": "Journal of Logical and Algebraic Methods in Programming",
    "jwe": "Journal of Web Engineering",
    "soca": "Service Oriented Computing and Applications",
    "sqj": "Software Quality Journal",
    "tplp": "Theory and Practice of Logic Programming",
    "pacmpl": "Proceedings of the ACM on Programming Languages",
    # 数据库/数据挖掘/内容检索
    "dpd": "Distributed and Parallel Databases",
    "i&m": "Information and Management",
    "ipm": "Information Processing & Management",
    "ipl": "Information Processing Letters",
    "jdm": "International Journal of Data Warehousing and Mining",
    "jgitm": "Journal of Global Information Technology Management",
    "jcst": "Journal of Computer Science and Technology",
    "wir data mining": "Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery",
    # 人工智能
    "npl": "Neural Processing Letters",
    "pattern recognition letters": "Pattern Recognition Letters",
    "eswa": "Expert Systems with Applications",
    "neurocomputing": "Neurocomputing",
    "eaai": "Engineering Applications of Artificial Intelligence",
    "kbs": "Knowledge-Based Systems",
    "applied intelligence": "Applied Intelligence",
    "mva": "Machine Vision and Applications",
    "iet cv": "IET Computer Vision",
    "ivc": "Image and Vision Computing",
    "csl": "Computer Speech & Language",
    "speech communication": "Speech Communication",
}


def _normalize_venue_name(venue: str) -> str:
    """
    标准化 venue 名称（小写、去除特殊字符）
    注意：保留 "transactions" 和 "journal" 用于区分期刊和会议
    """
    if not venue:
        return ""
    
    # 转小写
    venue = venue.lower()
    
    # 去除常见前缀（但保留 journal/transactions 用于类型判断）
    venue = re.sub(r'\b(the|international|conference|workshop|symposium)\b', '', venue)
    
    # 去除标点和多余空格
    venue = re.sub(r'[^\w\s]', '', venue)
    venue = venue.strip()
    
    # 去除多余空格
    venue = re.sub(r'\s+', ' ', venue)
    
    return venue


def _extract_venue_from_paper(paper: dict) -> Optional[str]:
    """
    从论文信息中提取发表 venue
    
    尝试多个字段：
    - venue (Semantic Scholar)
    - journal
    - conference
    - publication
    - booktitle
    """
    venue_fields = ["venue", "journal", "conference", "publication", "booktitle"]
    
    for field in venue_fields:
        venue = paper.get(field)
        if venue and isinstance(venue, str) and venue.strip():
            return venue.strip()
    
    return None


def _check_ccf_rank(venue: str) -> Optional[Tuple[str, str]]:
    """
    查询 venue 的 CCF 评级
    
    返回:
        Tuple[str, str]: (评级，类型) 例如 ("A", "conference")
        None: 未找到匹配
    
    匹配策略：
    1. 期刊优先于会议
    2. 更长、更具体的名称优先匹配
    3. 使用词边界匹配，避免短键名误匹配（如 "is" 匹配到 "Information Systems"）
    4. 按 CCF-A → B → C 顺序检查（高评级优先）
    """
    if not venue:
        return None
    
    normalized = _normalize_venue_name(venue)
    words = set(normalized.split())  # 将 venue 拆分为单词集合
    
    def match_key(key: str, text: str) -> bool:
        """
        精确匹配键名到文本
        - 如果键名包含空格，要求完整短语匹配
        - 如果键名是单个短词（<4 字符），要求是完整单词且文本长度足够
        - 如果键名是较长单词，允许子串匹配
        """
        key_normalized = _normalize_venue_name(key)
        
        # 完整匹配（最优先）
        if key_normalized == text:
            return True
        
        # 如果键名包含空格，要求完整短语出现在文本中
        if ' ' in key_normalized:
            return key_normalized in text
        
        # 对于短键名（<4 字符），要求是完整单词匹配
        if len(key_normalized) < 4:
            # 检查是否是完整单词
            return key_normalized in words
        
        # 对于较长键名，允许子串匹配
        return key_normalized in text
    
    # 构建所有期刊候选列表（按名称长度降序排序）
    journal_candidates = []
    for jour_key, jour_full in CCF_A_JOURNALS.items():
        journal_candidates.append((jour_key, "A", "journal"))
    for jour_key, jour_full in CCF_B_JOURNALS.items():
        journal_candidates.append((jour_key, "B", "journal"))
    for jour_key, jour_full in CCF_C_JOURNALS.items():
        journal_candidates.append((jour_key, "C", "journal"))
    
    # 构建所有会议候选列表
    conference_candidates = []
    for conf_key, conf_full in CCF_A_CONFERENCES.items():
        conference_candidates.append((conf_key, "A", "conference"))
    for conf_key, conf_full in CCF_B_CONFERENCES.items():
        conference_candidates.append((conf_key, "B", "conference"))
    for conf_key, conf_full in CCF_C_CONFERENCES.items():
        conference_candidates.append((conf_key, "C", "conference"))
    
    # 优先检查期刊（按名称长度降序排序，更具体的名称优先）
    journal_candidates.sort(key=lambda x: len(x[0]), reverse=True)
    for jour_key, rank, pub_type in journal_candidates:
        if match_key(jour_key, normalized):
            return (rank, pub_type)
    
    # 再检查会议（按名称长度降序排序）
    conference_candidates.sort(key=lambda x: len(x[0]), reverse=True)
    for conf_key, rank, pub_type in conference_candidates:
        if match_key(conf_key, normalized):
            return (rank, pub_type)
    
    return None


def _query_semantic_scholar(paper: dict) -> Optional[dict]:
    """
    通过 Semantic Scholar API 查询论文的发表信息
    
    支持多种查询方式：
    1. DOI 优先
    2. arXiv ID（从 URL 提取）
    3. 标题搜索（需要 API key，暂不支持）
    """
    title = paper.get("title", "")
    doi = paper.get("doi", "")
    url = paper.get("url", "")
    
    # 尝试从 arXiv URL 提取 arXiv ID
    arxiv_id = None
    if url and "arxiv.org/abs/" in url:
        # 提取 arXiv ID，去除版本号（如 v1, v2）
        arxiv_part = url.split("arxiv.org/abs/")[-1]
        arxiv_id = arxiv_part.split("/")[0].split("v")[0].strip()
    
    if not title and not doi and not arxiv_id:
        return None
    
    # 构建查询 URL（优先级：DOI > arXiv ID）
    api_url = None
    if doi:
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    elif arxiv_id:
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}"
    
    if not api_url:
        return None
    
    # 添加 fields 参数以获取完整的发表信息
    api_url += "?fields=title,venue,publicationDate,journal,publicationTypes"
    
    try:
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "paper-review-pro/1.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            # 验证返回数据是否完整
            if not data.get("paperId"):
                print(f"    [API 警告] 返回数据不完整，可能是速率限制")
                return None
            return data
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"    [API 速率限制] 等待 15 秒后重试...")
            import time
            time.sleep(15)
            try:
                req = urllib.request.Request(
                    api_url,
                    headers={"User-Agent": "paper-review-pro/1.0"}
                )
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    if not data.get("paperId"):
                        return None
                    return data
            except Exception:
                return None
        elif e.code == 404:
            # 论文未在 Semantic Scholar 中收录
            return None
        else:
            print(f"    [API HTTP 错误] {e.code}: {e.reason}")
            return None
    except Exception as e:
        print(f"    [API 查询失败] {type(e).__name__}: {e}")
        return None


def get_publication_status(paper: dict, use_api: bool = False) -> dict:
    """
    获取论文的发表状态
    
    参数:
        paper: dict，包含论文信息
        use_api: bool，是否使用在线 API 查询（默认 False，仅使用本地数据库）
    
    返回:
        dict: {
            "is_preprint": bool,  # 是否为预印本
            "publication": str,   # 发表 venue（如果有）
            "ccf_rank": str,      # CCF 评级 (A/B/C)，没有则为空
            "publication_type": str,  # "conference" | "journal" | "unknown"
            "confidence": str     # "high" | "medium" | "low"
        }
    """
    result = {
        "is_preprint": True,
        "publication": "",
        "ccf_rank": "",
        "publication_type": "unknown",
        "confidence": "low"
    }
    
    # 1. 从论文信息中提取 venue
    venue = _extract_venue_from_paper(paper)
    
    if venue:
        result["publication"] = venue
        result["is_preprint"] = False
        
        # 判断是会议还是期刊
        source = paper.get("source", "").lower()
        if "semantic" in source:
            # Semantic Scholar 通常会提供 venue 信息
            if paper.get("venue"):
                result["publication_type"] = "conference" if "conf" in paper.get("venue", "").lower() else "journal"
        
        # 2. 查询 CCF 评级
        ccf_result = _check_ccf_rank(venue)
        
        if ccf_result:
            result["ccf_rank"] = ccf_result[0]
            result["publication_type"] = ccf_result[1]
            result["confidence"] = "high"
        else:
            # 有 venue 但未匹配到 CCF 评级
            result["confidence"] = "medium"
    
    # 3. 检查是否是 arXiv 预印本
    url = paper.get("url", "").lower()
    source = paper.get("source", "").lower()
    
    if "arxiv" in url or "arxiv" in source:
        if not venue:
            result["is_preprint"] = True
            result["publication"] = ""
            result["ccf_rank"] = ""
            result["publication_type"] = "preprint"
            result["confidence"] = "high"
    
    # 4. 如果启用 API，尝试在线查询（可选）
    if use_api and result["is_preprint"]:
        print(f"    [API 查询] 正在查询 Semantic Scholar...")
        semantic_data = _query_semantic_scholar(paper)
        if semantic_data:
            s2_venue = semantic_data.get("venue")
            s2_journal = semantic_data.get("journal", {})
            
            # 优先使用 journal.name（更准确）
            if s2_journal and isinstance(s2_journal, dict) and s2_journal.get("name"):
                s2_venue = s2_journal["name"]
            
            if s2_venue:
                print(f"    [API 查询成功] 发现发表 venue: {s2_venue}")
                result["publication"] = s2_venue
                result["is_preprint"] = False
                
                ccf_result = _check_ccf_rank(s2_venue)
                if ccf_result:
                    result["ccf_rank"] = ccf_result[0]
                    result["publication_type"] = ccf_result[1]
                    result["confidence"] = "high"
                    print(f"    [CCF 匹配] {s2_venue} → CCF-{ccf_result[0]} ({ccf_result[1]})")
                else:
                    result["publication_type"] = "journal" if "journal" in str(semantic_data.get("publicationTypes", [])).lower() or "transaction" in s2_venue.lower() else "conference"
                    result["confidence"] = "medium"
                    print(f"    [CCF 匹配] 未找到 CCF 评级，但已确认发表在：{s2_venue}")
        else:
            print(f"    [API 查询失败] 未在 Semantic Scholar 中找到发表信息")
    
    return result


def calculate_authority_score(publication_status: dict) -> float:
    """
    根据发表状态计算权威度分数（0.0 - 1.0）
    
    评分标准：
    - CCF-A 类：1.0
    - CCF-B 类：0.8
    - CCF-C 类：0.6
    - 已发表但未评级：0.5
    - 预印本：0.3
    
    返回:
        float: 权威度分数
    """
    ccf_rank = publication_status.get("ccf_rank", "")
    is_preprint = publication_status.get("is_preprint", True)
    publication = publication_status.get("publication", "")
    
    if ccf_rank == "A":
        return 1.0
    elif ccf_rank == "B":
        return 0.8
    elif ccf_rank == "C":
        return 0.6
    elif publication and not is_preprint:
        # 已发表但未匹配到 CCF 评级
        return 0.5
    else:
        # 预印本
        return 0.3


def enrich_papers_with_publication_status(papers: list, use_api: bool = False) -> list:
    """
    批量为论文添加发表状态信息
    
    参数:
        papers: list of dict，论文列表
        use_api: bool，是否使用在线 API
    
    返回:
        list of dict: 添加了 publication_status 字段的论文列表
    """
    enriched_papers = []
    
    print("\n=== 查询发表状态 ===")
    
    for i, paper in enumerate(papers, 1):
        print(f"  [{i}/{len(papers)}] {paper.get('title', 'Unknown')[:50]}...")
        
        pub_status = get_publication_status(paper, use_api=use_api)
        
        # 将发表状态信息合并到论文字典中
        paper["is_preprint"] = pub_status["is_preprint"]
        paper["publication"] = pub_status["publication"]
        paper["ccf_rank"] = pub_status["ccf_rank"]
        paper["publication_type"] = pub_status["publication_type"]
        paper["authority_score"] = calculate_authority_score(pub_status)
        
        # 显示结果
        status_str = f"CCF-{pub_status['ccf_rank']}" if pub_status['ccf_rank'] else "未评级"
        if pub_status['is_preprint']:
            status_str = "preprint"
        
        print(f"    → {status_str} (权威度：{paper['authority_score']:.1f})")
        
        enriched_papers.append(paper)
    
    return enriched_papers


def get_ccf_database_stats() -> dict:
    """
    获取 CCF 数据库统计信息
    
    返回:
        dict: 包含各类别数量的统计信息
    """
    return {
        "conferences": {
            "A": len(CCF_A_CONFERENCES),
            "B": len(CCF_B_CONFERENCES),
            "C": len(CCF_C_CONFERENCES),
        },
        "journals": {
            "A": len(CCF_A_JOURNALS),
            "B": len(CCF_B_JOURNALS),
            "C": len(CCF_C_JOURNALS),
        },
        "total": {
            "conferences": len(CCF_A_CONFERENCES) + len(CCF_B_CONFERENCES) + len(CCF_C_CONFERENCES),
            "journals": len(CCF_A_JOURNALS) + len(CCF_B_JOURNALS) + len(CCF_C_JOURNALS),
            "all": len(CCF_A_CONFERENCES) + len(CCF_B_CONFERENCES) + len(CCF_C_CONFERENCES) + 
                   len(CCF_A_JOURNALS) + len(CCF_B_JOURNALS) + len(CCF_C_JOURNALS),
        }
    }


def main():
    """
    命令行测试入口
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="论文发表状态查询测试")
    parser.add_argument("--title", type=str, required=True, help="论文标题")
    parser.add_argument("--venue", type=str, default="", help="发表 venue")
    parser.add_argument("--source", type=str, default="arxiv", help="来源 (arxiv/semantic)")
    parser.add_argument("--url", type=str, default="", help="论文 URL")
    parser.add_argument("--use-api", action="store_true", help="使用在线 API 查询")
    parser.add_argument("--stats", action="store_true", help="显示 CCF 数据库统计")
    
    args = parser.parse_args()
    
    if args.stats:
        stats = get_ccf_database_stats()
        print("\n=== CCF 数据库统计（第七版，2026 年 3 月）===")
        print(f"\n会议:")
        print(f"  CCF-A: {stats['conferences']['A']} 个")
        print(f"  CCF-B: {stats['conferences']['B']} 个")
        print(f"  CCF-C: {stats['conferences']['C']} 个")
        print(f"\n期刊:")
        print(f"  CCF-A: {stats['journals']['A']} 个")
        print(f"  CCF-B: {stats['journals']['B']} 个")
        print(f"  CCF-C: {stats['journals']['C']} 个")
        print(f"\n总计:")
        print(f"  会议：{stats['total']['conferences']} 个")
        print(f"  期刊：{stats['total']['journals']} 个")
        print(f"  全部：{stats['total']['all']} 个")
        return
    
    paper = {
        "title": args.title,
        "venue": args.venue,
        "source": args.source,
        "url": args.url
    }
    
    result = get_publication_status(paper, use_api=args.use_api)
    
    print("\n=== 发表状态 ===")
    print(f"  预印本：{'是' if result['is_preprint'] else '否'}")
    print(f"  发表 venue: {result['publication'] or '无'}")
    print(f"  CCF 评级：{result['ccf_rank'] or '未评级'}")
    print(f"  类型：{result['publication_type']}")
    print(f"  置信度：{result['confidence']}")
    print(f"  权威度分数：{calculate_authority_score(result):.2f}")


if __name__ == "__main__":
    main()
