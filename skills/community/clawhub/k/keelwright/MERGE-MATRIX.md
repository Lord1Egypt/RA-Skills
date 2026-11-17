# MERGE-MATRIX — слияние результатов роя аудита keelwright

> Как объединить 16 ответов агентов в один отчёт. Статус: рабочий.

## Легенда уровней
- **critical** — обход гейта / утечка секрета / сломанный механизм защиты
- **major** — противоречие между файлами / неработающий скрипт / лицензионный конфликт
- **minor** — опечатка / неясная формулировка / missing doc
- **OK** — проблем не найдено

## Правила слияния
1. **Dedupe**: если обе модели (hy3 + step 3.7) нашли одно и то же → один пункт,
   пометить «подтверждено 2 моделями».
2. **Conflict**: если модели противоречат (одна OK, другая нашла) → эскалация
   оркестратору, третья проверка вручную.
3. **Group by роль**: в AUDIT-RESULTS.md секции по 8 ролям.
4. **Итоговая таблица**: critical / major / minor / OK counts.
5. **Приоритет исправлений**: critical → major → minor.

## Матрица ролей → что проверяют
| Роль | Фокус |
|------|-------|
| ai-generated-code-security-auditor | гейты, инъекции, секреты |
| compliance-auditor | лицензии, white-list, атрибуция |
| code-reviewer | логика, целостность, противоречия |
| legal-document-review | авторство, copyright |
| python-code-auditor | scripts/*.py работоспособность |
| documentation-consistency-auditor | SKILL.md ↔ references ↔ README |
| runtime-agnostic-auditor | хардкод путей/рантаймов |
| security-gates-auditor | 28 gates обход |
