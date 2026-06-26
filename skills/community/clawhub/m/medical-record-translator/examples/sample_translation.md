# Medical Record Translation Structural Smoke Test

### [P1-B1] title
中文：
出院记录翻译样例

原文：
Discharge Summary Translation Sample

### [P1-B2] paragraph
中文：
患者因肺部感染入院，抗感染治疗后体温恢复正常，生命体征平稳。

原文：
The patient was admitted for pulmonary infection. Temperature returned to normal after anti-infective treatment and vital signs remained stable.

### [P1-B3] table
<table>
  <tr><th>字段</th><th>中文</th><th>原文</th></tr>
  <tr><td>过敏史</td><td>青霉素过敏</td><td>Penicillin allergy</td></tr>
  <tr><td>用药剂量</td><td>[低置信度] 疑似 0.25 mg，需核对原件</td><td>[低置信度] appears to read 0.25 mg</td></tr>
</table>

## 需重点核对项

- `[P1-B3]` 用药剂量为 `[低置信度]` 项，建议对照原件复核。
