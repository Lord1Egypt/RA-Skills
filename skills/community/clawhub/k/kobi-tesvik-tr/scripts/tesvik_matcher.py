#!/usr/bin/env python3
"""
tesvik_matcher.py — Türkiye KOBİ Teşvik Eşleştirici
Sektör, çalışan sayısı ve ciro bilgisine göre uygun teşvikleri listeler.

Geliştiren: Finhouse (finhouse.ai)
Lisans: Apache-2.0
"""

import argparse
import sys

# ──────────────────────────────────────────────────────
# Teşvik veritabanı
# ──────────────────────────────────────────────────────

KOSGEB_PROGRAMLAR = [
    {
        "ad": "Dijital Dönüşüm Desteği",
        "aciklama": "ERP, CRM, e-ticaret, bulut, yapay zeka yatırımları",
        "max_tutar": "500.000 - 2.000.000 TL (büyüklüğe göre)",
        "oran": "%60-75",
        "sure": "12-24 ay",
        "kobi_tipleri": ["mikro", "kucuk", "orta"],
        "sektorler": ["tumu"],
        "url": "https://www.kosgeb.gov.tr",
        "geri_odeme": False,
    },
    {
        "ad": "Yeni Girişimci Desteği",
        "aciklama": "1 yıldan az süreli işletmeler için kuruluş ve kira desteği",
        "max_tutar": "250.000 TL (geri ödemesiz) + 150.000 TL (geri ödemeli)",
        "oran": "%100",
        "sure": "24 ay",
        "kobi_tipleri": ["mikro"],
        "sektorler": ["tumu"],
        "url": "https://www.kosgeb.gov.tr",
        "geri_odeme": False,
        "yeni_sirket": True,
    },
    {
        "ad": "AR-GE ve İnovasyon Desteği",
        "aciklama": "Yeni ürün/süreç geliştirme projeleri",
        "max_tutar": "5.000.000 TL",
        "oran": "%75",
        "sure": "24 ay",
        "kobi_tipleri": ["mikro", "kucuk", "orta"],
        "sektorler": ["yazilim", "imalat", "saglik", "fintech", "teknoloji"],
        "url": "https://www.kosgeb.gov.tr",
        "geri_odeme": False,
    },
    {
        "ad": "İhracat Pazarlama Desteği",
        "aciklama": "Yurt dışı pazar araştırma ve fuar katılımı",
        "max_tutar": "200.000 TL/yıl",
        "oran": "%70",
        "sure": "12 ay",
        "kobi_tipleri": ["mikro", "kucuk", "orta"],
        "sektorler": ["tumu"],
        "url": "https://www.kosgeb.gov.tr",
        "geri_odeme": False,
    },
    {
        "ad": "Faizsiz İşletme Kredisi",
        "aciklama": "KOSGEB destekli faizsiz/düşük faizli kredi",
        "max_tutar": "2.000.000 TL",
        "oran": "Faiz desteği",
        "sure": "48 ay",
        "kobi_tipleri": ["mikro", "kucuk", "orta"],
        "sektorler": ["tumu"],
        "url": "https://www.kosgeb.gov.tr",
        "geri_odeme": True,
    },
]

TUBITAK_PROGRAMLAR = [
    {
        "ad": "1507 — KOBİ AR-GE Başlangıç",
        "aciklama": "AR-GE'ye başlayan KOBİ'ler için kolay başvuru",
        "max_tutar": "1.800.000 TL",
        "oran": "%75",
        "sure": "18 ay",
        "kobi_tipleri": ["mikro", "kucuk"],
        "sektorler": ["yazilim", "fintech", "teknoloji", "imalat", "saglik"],
        "url": "https://www.tubitak.gov.tr/1507",
        "geri_odeme": False,
    },
    {
        "ad": "1501 — Sanayi AR-GE",
        "aciklama": "Büyük AR-GE projeler, tüm şirket büyüklükleri",
        "max_tutar": "15.000.000 TL",
        "oran": "%75 (KOBİ) / %60 (büyük)",
        "sure": "36 ay",
        "kobi_tipleri": ["kucuk", "orta"],
        "sektorler": ["yazilim", "fintech", "teknoloji", "imalat", "saglik", "enerji"],
        "url": "https://www.tubitak.gov.tr/1501",
        "geri_odeme": False,
    },
    {
        "ad": "1512 — BiGG (Bireysel Genç Girişimci)",
        "aciklama": "Teknoloji girişimcisi adayları için kuluçka + hibe",
        "max_tutar": "900.000 TL (2 faz)",
        "oran": "%100",
        "sure": "18 ay",
        "kobi_tipleri": ["mikro"],
        "sektorler": ["yazilim", "fintech", "teknoloji", "saglik"],
        "url": "https://www.tubitak.gov.tr/bigg",
        "geri_odeme": False,
        "yeni_sirket": True,
    },
    {
        "ad": "1511 — Öncelikli Alan AR-GE",
        "aciklama": "Yapay zeka, siber güvenlik, yeşil teknoloji odaklı",
        "max_tutar": "20.000.000 TL",
        "oran": "%75",
        "sure": "36 ay",
        "kobi_tipleri": ["kucuk", "orta"],
        "sektorler": ["yazilim", "fintech", "teknoloji", "enerji", "savunma"],
        "url": "https://www.tubitak.gov.tr/1511",
        "geri_odeme": False,
    },
]

ISKUR_TESVIKLER = [
    {
        "ad": "Genç İstihdam Teşviki",
        "aciklama": "18-29 yaş çalışan için SGK işveren payı Hazine'den",
        "max_tutar": "SGK işveren payının tamamı",
        "oran": "%100",
        "sure": "6-54 ay",
        "kobi_tipleri": ["mikro", "kucuk", "orta"],
        "sektorler": ["tumu"],
        "url": "https://www.iskur.gov.tr",
        "geri_odeme": False,
    },
    {
        "ad": "Uzun Süreli İşsiz Teşviki",
        "aciklama": "6+ ay işsiz kişi istihdamında SGK desteği",
        "max_tutar": "SGK işveren payının tamamı",
        "oran": "%100",
        "sure": "12 ay",
        "kobi_tipleri": ["mikro", "kucuk", "orta"],
        "sektorler": ["tumu"],
        "url": "https://www.iskur.gov.tr",
        "geri_odeme": False,
    },
    {
        "ad": "Engelli İstihdam Teşviki",
        "aciklama": "Engelli çalışan başına SGK tam desteği",
        "max_tutar": "SGK işveren payının tamamı",
        "oran": "%100",
        "sure": "Süresiz",
        "kobi_tipleri": ["mikro", "kucuk", "orta"],
        "sektorler": ["tumu"],
        "url": "https://www.iskur.gov.tr",
        "geri_odeme": False,
    },
]

VERGI_MUAFIYETLERI = [
    {
        "ad": "AR-GE İndirimi",
        "aciklama": "AR-GE harcamalarının %100-150'si vergiden indirim",
        "max_tutar": "Sınırsız",
        "oran": "%100 (normal) / %150 (AR-GE merkezi)",
        "sektorler": ["yazilim", "fintech", "teknoloji", "imalat"],
        "url": "https://www.gib.gov.tr",
    },
    {
        "ad": "Teknokent Kurumlar Vergisi Muafiyeti",
        "aciklama": "Teknokent'te yazılım/AR-GE gelirlerinde %100 KV muafiyet",
        "max_tutar": "Tüm AR-GE/yazılım gelirleri",
        "oran": "%100",
        "sektorler": ["yazilim", "fintech", "teknoloji"],
        "url": "https://www.teknokent.gov.tr",
    },
    {
        "ad": "KDV İstisnası — Yazılım",
        "aciklama": "Teknokent'te geliştirilen yazılımın yurt içi satışında KDV yok",
        "max_tutar": "Tüm yazılım satışları",
        "oran": "%0",
        "sektorler": ["yazilim", "fintech", "teknoloji"],
        "url": "https://www.gib.gov.tr",
    },
]

# ──────────────────────────────────────────────────────
# Yardımcı fonksiyonlar
# ──────────────────────────────────────────────────────

SEKTORLER = [
    "yazilim", "fintech", "teknoloji", "imalat", "saglik",
    "tarim", "turizm", "enerji", "lojistik", "ticaret",
    "hizmet", "insaat", "gida", "tekstil", "savunma", "diger"
]

def kobi_tipi_belirle(calisanlar: int, ciro_tl: float) -> str:
    if calisanlar <= 9 and ciro_tl <= 25_000_000:
        return "mikro"
    elif calisanlar <= 49 and ciro_tl <= 100_000_000:
        return "kucuk"
    elif calisanlar <= 249 and ciro_tl <= 500_000_000:
        return "orta"
    else:
        return "buyuk"

def sektor_eslesir(program_sektorler: list, sektor: str) -> bool:
    if "tumu" in program_sektorler:
        return True
    return sektor.lower() in program_sektorler

def kobi_tipi_eslesir(program_tipler: list, tip: str) -> bool:
    return tip in program_tipler

def tesvikleri_bul(sektor: str, calisanlar: int, ciro_tl: float, yeni_sirket: bool = False) -> dict:
    kobi_tip = kobi_tipi_belirle(calisanlar, ciro_tl)
    sonuclar = {
        "kobi_tipi": kobi_tip,
        "kosgeb": [],
        "tubitak": [],
        "iskur": [],
        "vergi": [],
    }

    if kobi_tip == "buyuk":
        return sonuclar  # KOSGEB/TÜBITAK KOBİ programları uygulanmaz

    for p in KOSGEB_PROGRAMLAR:
        if yeni_sirket and not p.get("yeni_sirket", False) and p["ad"] == "Yeni Girişimci Desteği":
            continue
        if kobi_tipi_eslesir(p["kobi_tipleri"], kobi_tip) and sektor_eslesir(p["sektorler"], sektor):
            sonuclar["kosgeb"].append(p)

    for p in TUBITAK_PROGRAMLAR:
        if kobi_tipi_eslesir(p["kobi_tipleri"], kobi_tip) and sektor_eslesir(p["sektorler"], sektor):
            sonuclar["tubitak"].append(p)

    for p in ISKUR_TESVIKLER:
        if kobi_tipi_eslesir(p["kobi_tipleri"], kobi_tip):
            sonuclar["iskur"].append(p)

    for p in VERGI_MUAFIYETLERI:
        if sektor_eslesir(p["sektorler"], sektor):
            sonuclar["vergi"].append(p)

    return sonuclar

def yazdir_program(p: dict, index: int):
    geri = "✅ Geri ödemesiz hibe" if not p.get("geri_odeme", True) else "🔄 Geri ödemeli kredi"
    print(f"  {index}. {p['ad']}")
    print(f"     {geri}")
    print(f"     📋 {p['aciklama']}")
    print(f"     💰 Üst limit: {p['max_tutar']}")
    print(f"     📊 Destek oranı: {p['oran']}")
    if "sure" in p:
        print(f"     ⏱  Süre: {p['sure']}")
    print(f"     🔗 {p['url']}")
    print()

def yazdir_sonuclar(sonuclar: dict, sektor: str, calisanlar: int, ciro_tl: float):
    print("\n" + "═" * 60)
    print("  KOBİ TEŞVİK EŞLEŞME RAPORU")
    print("  Powered by Finhouse.ai")
    print("═" * 60)
    print(f"  Sektör    : {sektor}")
    print(f"  Çalışan   : {calisanlar}")
    print(f"  Ciro      : {ciro_tl:,.0f} TL")
    print(f"  KOBİ Tipi : {sonuclar['kobi_tipi'].upper()}")
    print("═" * 60)

    toplam = sum(len(v) for k, v in sonuclar.items() if k != "kobi_tipi")
    print(f"\n  ✨ Toplam {toplam} uygun program bulundu!\n")

    if sonuclar["kosgeb"]:
        print(f"┌─ KOSGEB ({len(sonuclar['kosgeb'])} program)")
        for i, p in enumerate(sonuclar["kosgeb"], 1):
            yazdir_program(p, i)

    if sonuclar["tubitak"]:
        print(f"┌─ TÜBİTAK ({len(sonuclar['tubitak'])} program)")
        for i, p in enumerate(sonuclar["tubitak"], 1):
            yazdir_program(p, i)

    if sonuclar["iskur"]:
        print(f"┌─ İŞKUR TEŞVİKLERİ ({len(sonuclar['iskur'])} program)")
        for i, p in enumerate(sonuclar["iskur"], 1):
            yazdir_program(p, i)

    if sonuclar["vergi"]:
        print(f"┌─ VERGİ MUAFİYETLERİ ({len(sonuclar['vergi'])} program)")
        for i, p in enumerate(sonuclar["vergi"], 1):
            yazdir_program(p, i)

    print("─" * 60)
    print("⚠️  Not: Tutarlar tahminidir. Başvuru öncesi resmi kaynakları")
    print("   kontrol edin. Programların başvuru dönemleri değişebilir.")
    print()
    print("💡 Finhouse danışmanlık: finhouse.ai | info@finhouse.ai")
    print("─" * 60 + "\n")

def interaktif_mod():
    print("\n🔍 KOBİ Teşvik Eşleştirici — Finhouse.ai\n")
    print("Sektörünüzü seçin:")
    for i, s in enumerate(SEKTORLER, 1):
        print(f"  {i:2}. {s}")
    
    while True:
        secim = input("\nSektör numarası (1-17): ").strip()
        if secim.isdigit() and 1 <= int(secim) <= len(SEKTORLER):
            sektor = SEKTORLER[int(secim) - 1]
            break
        print("Geçersiz seçim, tekrar deneyin.")

    while True:
        calisanlar_str = input("Çalışan sayısı: ").strip()
        if calisanlar_str.isdigit():
            calisanlar = int(calisanlar_str)
            break
        print("Sayı girin.")

    while True:
        ciro_str = input("Yıllık ciro (TL, örn: 5000000): ").strip().replace(",", "").replace(".", "")
        if ciro_str.isdigit():
            ciro_tl = float(ciro_str)
            break
        print("Sayı girin.")

    sonuclar = tesvikleri_bul(sektor, calisanlar, ciro_tl)
    yazdir_sonuclar(sonuclar, sektor, calisanlar, ciro_tl)

# ──────────────────────────────────────────────────────
# Ana program
# ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Türkiye KOBİ Teşvik Eşleştirici — Finhouse.ai",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--sektor", type=str, help=f"Sektör: {', '.join(SEKTORLER)}")
    parser.add_argument("--calisanlar", type=int, help="Çalışan sayısı")
    parser.add_argument("--ciro", type=float, help="Yıllık ciro (TL)")
    parser.add_argument("--il", type=str, default="istanbul", help="İl (kalkınma ajansı için)")
    parser.add_argument("--interaktif", action="store_true", help="İnteraktif mod")

    args = parser.parse_args()

    if args.interaktif or (not args.sektor and not args.calisanlar):
        interaktif_mod()
        return

    if not args.sektor or not args.calisanlar or not args.ciro:
        parser.print_help()
        print("\nHata: --sektor, --calisanlar ve --ciro parametreleri zorunludur.")
        sys.exit(1)

    sonuclar = tesvikleri_bul(args.sektor, args.calisanlar, args.ciro)
    yazdir_sonuclar(sonuclar, args.sektor, args.calisanlar, args.ciro)

if __name__ == "__main__":
    main()
