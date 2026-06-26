#!/usr/bin/env python3
"""
Download tariff PDF from Philippines Tariff Commission website.
Uses Playwright to handle WAF protection.
"""

import asyncio
import sys
import os
import subprocess

# Chapter mapping for common product categories
CHAPTER_MAP = {
    "01": "Live animals",
    "02": "Meat and edible meat offal",
    "03": "Fish and crustaceans",
    "04": "Dairy produce",
    "05": "Products of animal origin",
    "06": "Live trees and other plants",
    "07": "Edible vegetables",
    "08": "Edible fruit and nuts",
    "09": "Coffee, tea, spices",
    "10": "Cereals",
    "11": "Products of the milling industry",
    "12": "Oil seeds and oleaginous fruits",
    "13": "Lac, gums, resins",
    "14": "Vegetable plaiting materials",
    "15": "Animal or vegetable fats and oils",
    "16": "Preparations of meat, fish",
    "17": "Sugars and sugar confectionery",
    "18": "Cocoa and cocoa preparations",
    "19": "Preparations of cereals, flour",
    "20": "Preparations of vegetables, fruit",
    "21": "Miscellaneous edible preparations",
    "22": "Beverages, spirits and vinegar",
    "23": "Residues and waste from food industries",
    "24": "Tobacco and tobacco substitutes",
    "25": "Salt, sulphur, earths and stone",
    "26": "Ores, slag and ash",
    "27": "Mineral fuels, mineral oils",
    "28": "Inorganic chemicals",
    "29": "Organic chemicals",
    "30": "Pharmaceutical products",
    "31": "Fertilizers",
    "32": "Tanning or dyeing extracts",
    "33": "Essential oils and resinoids",
    "34": "Soap, organic surface-active agents",
    "35": "Albuminoidal substances",
    "36": "Explosives, pyrotechnic products",
    "37": "Photographic or cinematographic goods",
    "38": "Miscellaneous chemical products",
    "39": "Plastics and articles thereof",
    "40": "Rubber and articles thereof",
    "41": "Raw hides and skins",
    "42": "Articles of leather",
    "43": "Furskins and artificial fur",
    "44": "Wood and articles of wood",
    "45": "Cork and articles of cork",
    "46": "Manufactures of straw, esparto",
    "47": "Pulp of wood, fibrous cellulosic material",
    "48": "Paper and paperboard",
    "49": "Printed books, newspapers, pictures",
    "50": "Silk",
    "51": "Wool, fine or coarse animal hair",
    "52": "Cotton",
    "53": "Other vegetable textile fibres",
    "54": "Man-made filaments",
    "55": "Man-made staple fibres",
    "56": "Wadding, felt and nonwovens",
    "57": "Carpets and other textile floor coverings",
    "58": "Special woven fabrics",
    "59": "Impregnated, coated, covered or laminated textile fabrics",
    "60": "Knitted or crocheted fabrics",
    "61": "Articles of apparel, knitted or crocheted",
    "62": "Articles of apparel, not knitted or crocheted",
    "63": "Other made up textile articles",
    "64": "Footwear, gaiters and the like",
    "65": "Headgear and parts thereof",
    "66": "Umbrellas, sun umbrellas, walking-sticks",
    "67": "Prepared feathers and down",
    "68": "Articles of stone, plaster, cement",
    "69": "Ceramic products",
    "70": "Glass and glassware",
    "71": "Natural or cultured pearls, precious stones",
    "72": "Iron and steel",
    "73": "Articles of iron or steel",
    "74": "Copper and articles thereof",
    "75": "Nickel and articles thereof",
    "76": "Aluminium and articles thereof",
    "77": "(Reserved for possible future use)",
    "78": "Lead and articles thereof",
    "79": "Zinc and articles thereof",
    "80": "Tin and articles thereof",
    "81": "Other base metals",
    "82": "Tools, implements, cutlery",
    "83": "Miscellaneous articles of base metal",
    "84": "Nuclear reactors, boilers, machinery",
    "85": "Electrical machinery and equipment",
    "86": "Railway or tramway locomotives",
    "87": "Vehicles other than railway or tramway",
    "88": "Aircraft, spacecraft",
    "89": "Ships, boats and floating structures",
    "90": "Optical, photographic, cinematographic",
    "91": "Clocks and watches",
    "92": "Musical instruments",
    "93": "Arms and ammunition",
    "94": "Furniture, bedding, mattresses",
    "95": "Toys, games and sports requisites",
    "96": "Miscellaneous manufactured articles",
    "97": "Works of art, collectors' pieces",
}


def get_chapter_description(chapter_num: str) -> str:
    """Get description for a chapter number."""
    return CHAPTER_MAP.get(chapter_num.zfill(2), "Unknown category")


def find_chapters_by_keyword(keyword: str) -> list:
    """Find chapters matching a keyword."""
    keyword_lower = keyword.lower()
    matches = []
    for chapter, description in CHAPTER_MAP.items():
        if keyword_lower in description.lower():
            matches.append((chapter, description))
    return matches


def download_pdf_with_curl(chapter: str, output_dir: str = ".") -> str:
    """Download PDF using curl as fallback."""
    chapter_padded = chapter.zfill(2)
    pdf_url = f"https://www.tariffcommission.gov.ph/documents/tariff/2022/Chapter%20{chapter_padded}.pdf"
    output_path = os.path.join(output_dir, f"Chapter_{chapter_padded}.pdf")
    
    try:
        result = subprocess.run([
            "curl", "-s", "-L", "-A", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "-o", output_path, pdf_url
        ], capture_output=True, text=True, timeout=60)
        
        # Check if file was downloaded and is valid PDF
        if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            with open(output_path, 'rb') as f:
                header = f.read(4)
                if header == b'%PDF':
                    print(f"Downloaded: {output_path}")
                    return output_path
        
        print(f"Download failed or file is not a valid PDF")
        return ""
    except Exception as e:
        print(f"Error downloading with curl: {e}")
        return ""


async def download_pdf_with_playwright(chapter: str, output_dir: str = ".") -> str:
    """Download PDF using Playwright."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return ""
    
    chapter_padded = chapter.zfill(2)
    pdf_url = f"https://www.tariffcommission.gov.ph/documents/tariff/2022/Chapter%20{chapter_padded}.pdf"
    output_path = os.path.join(output_dir, f"Chapter_{chapter_padded}.pdf")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        try:
            response = await page.goto(pdf_url, wait_until="networkidle", timeout=60000)
            
            if response and response.status == 200:
                pdf_content = await response.body()
                with open(output_path, "wb") as f:
                    f.write(pdf_content)
                print(f"Downloaded: {output_path}")
                return output_path
            else:
                print(f"Failed to download Chapter {chapter_padded}: HTTP {response.status if response else 'No response'}")
                return ""
        except Exception as e:
            print(f"Error downloading Chapter {chapter_padded}: {e}")
            return ""
        finally:
            await browser.close()


async def download_pdf(chapter: str, output_dir: str = ".") -> str:
    """
    Download a tariff PDF for a specific chapter.
    
    Args:
        chapter: Chapter number (01-97)
        output_dir: Directory to save the PDF
        
    Returns:
        Path to downloaded file or empty string if failed
    """
    chapter_padded = chapter.zfill(2)
    pdf_url = f"https://www.tariffcommission.gov.ph/documents/tariff/2022/Chapter%20{chapter_padded}.pdf"
    
    # Try curl first (faster, no dependencies)
    result = download_pdf_with_curl(chapter, output_dir)
    if result:
        return result
    
    # Try playwright if available
    try:
        result = await download_pdf_with_playwright(chapter, output_dir)
        if result:
            return result
    except ImportError:
        pass
    
    print(f"\nNote: The website has WAF protection that may block automated downloads.")
    print(f"Please manually download the PDF from:")
    print(f"  {pdf_url}")
    print(f"\nThen provide the downloaded file for HS code search.")
    return ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: download_tariff_pdf.py <chapter_number> [output_directory]")
        print("\nExamples:")
        print("  python download_tariff_pdf.py 84")
        print("  python download_tariff_pdf.py 84 /path/to/save")
        sys.exit(1)
    
    chapter = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    result = asyncio.run(download_pdf(chapter, output_dir))
    print(result)
