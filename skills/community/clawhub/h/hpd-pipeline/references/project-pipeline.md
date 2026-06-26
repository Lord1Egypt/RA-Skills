# HPD pipeline

**Tüm çıktılar Türkçe olmalıdır.** Brief, BOM, assembly plan, tester report, completion summary — hepsi Türkçe yazılır. Teknik terimler (BOM, CAD, STL) İngilizce kalabilir ama açıklamaları Türkçe olur.

Stage order:

1. Planner
2. Designer
3. Developer when the idea needs electronics or software
4. Tester

Planner output (Türkçe):

- problem statement (sorun tanımı)
- target user (hedef kullanıcı)
- BOM (malzeme listesi, Türkçe açıklamalar)
- cost estimate (maliyet tahmini, TL ve USD)
- build assumptions (üretim varsayımları)

Designer output (Türkçe):

- assembly plan (montaj planı, Türkçe adımlar)
- visual direction (görsel yön)
- render prompt (İngilizce kalabilir — görsel AI için)
- render image: MUTLAKA üretilmeli. `openclaw image generate` komutunu dene; başarısız olursa Gemini API scriptini çalıştır.
- OpenSCAD code: Her proje için temel bir OpenSCAD parametrik taslak üret ve workspace'e kaydet (`design.scad`). Exact geometry gerekmez, ölçülendirme ve temel form yeterli.
- CAD artifact paths when actually produced

Developer output (Türkçe):

- architecture note (mimari not)
- firmware or software scope (yazılım kapsamı)
- interfaces and risks (arayüzler ve riskler)
- source code path when actually produced
- firmware build path when actually produced

Tester output (Türkçe):

- idea-to-output consistency check (fikir-çıktı uyumluluk kontrolü)
- missing assumptions (eksik varsayımlar)
- blocker list (blokerlar)
- final verdict (son karar)
- explicit actual-vs-conceptual artifact check (gerçek vs kavramsal kontrol)
- completion summary for owner handoff (sahip teslim özeti)
