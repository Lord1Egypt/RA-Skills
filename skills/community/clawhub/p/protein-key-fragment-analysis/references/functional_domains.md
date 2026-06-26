# 蛋白家族已知功能域参考

## 如何使用本文件

分析新蛋白家族时，在 `protein_key_fragment_analysis.py` 的以下两个配置中添加对应信息：

1. **KNOWN_MOTIFS** - 保守氨基酸模式（单残基或短序列）
2. **CONSERVED_BLOCKS** - 保守序列块（5-10aa）

---

## 配置示例

### 示例1：丝氨酸蛋白酶家族（Pfam S1）

```python
KNOWN_MOTIFS = {
    "催化三联体_His": {
        "pattern": ["H"],
        "context_note": "催化三联体组氨酸（His57，胰凝乳蛋白酶编号）",
        "function": "形成催化三联体，提取质子，激活亲核Ser",
        "criticality": "极关键"
    },
    "催化三联体_Asp": {
        "pattern": ["D"],
        "context_note": "催化三联体天冬氨酸（Asp102）",
        "function": "定向并稳定催化His的构象",
        "criticality": "极关键"
    },
    "催化三联体_Ser": {
        "pattern": ["S"],
        "context_note": "催化三联体丝氨酸（Ser195）",
        "function": "亲核攻击底物肽键，形成酰基-酶中间体",
        "criticality": "极关键"
    },
    "二硫键_Cys": {
        "pattern": ["C"],
        "context_note": "保守半胱氨酸对",
        "function": "形成二硫键，稳定蛋白三维结构",
        "criticality": "结构关键"
    }
}

CONSERVED_BLOCKS = {
    "His_block": "GDSGGP",       # 催化His附近的高保守块
    "Ser_block": "GDSG",         # Ser195周围
    "activation_Ile": "IVGG",    # 酶原激活位点
    "substrate_Asp": "GICAG",    # S1口袋相关
}
```

### 示例2：激酶家族

```python
KNOWN_MOTIFS = {
    "ATP结合位点_Lys": {
        "pattern": ["K"],
        "context_note": "保守赖氨酸，结合ATP的α/β磷酸",
        "function": "稳定ATP结合，参与磷酸转移",
        "criticality": "极关键"
    },
    "催化核心_Asp": {
        "pattern": ["D"],
        "context_note": "保守天冬氨酸，协调Mg²⁺离子",
        "function": "催化核心，参与磷酸基团转移",
        "criticality": "极关键"
    }
}

CONSERVED_BLOCKS = {
    "GxGxxG_motif": "GXGXXG",    # ATP结合口袋
    "HRD_motif": "HRDL",         # 催化环
    "DFG_motif": "DFG",          # 激活环起始
}
```

### 示例3：锌指蛋白家族

```python
KNOWN_MOTIFS = {
    "锌配位_Cys": {
        "pattern": ["C"],
        "context_note": "锌离子配位半胱氨酸",
        "function": "与His共同配位Zn²⁺，稳定DNA结合域",
        "criticality": "极关键"
    },
    "锌配位_His": {
        "pattern": ["H"],
        "context_note": "锌离子配位组氨酸",
        "function": "与Cys共同配位Zn²⁺",
        "criticality": "极关键"
    }
}

CONSERVED_BLOCKS = {
    "C2H2_zf": "CX4CX12HX4H",    # 经典C2H2锌指
    "C4_zf": "CX2CX13CX2CX14",   # 核受体C4锌指
}
```

---

## 数据来源

- **Pfam**: http://pfam.xfam.org/
- **InterPro**: https://www.ebi.ac.uk/interpro/
- **UniProt**: https://www.uniprot.org/
- **PROSITE**: https://prosite.expasy.org/

---

## 功能重要性分级

| 级别 | 标记 | 说明 |
|------|------|------|
| 极关键 | 🔴 | 直接参与催化/核心功能的残基 |
| 关键 | 🟠 | 影响底物特异性或调控的残基 |
| 结构关键 | 🟡 | 维持结构稳定性（二硫键、疏水核心等） |
| 高保守待确认 | 🔵 | 高度保守但功能待实验验证的残基 |
