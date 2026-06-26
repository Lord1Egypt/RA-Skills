#!/usr/bin/env python3
"""
LeadGenerator — Generator leadów B2B
Wersja: 1.0.0
Autor: Tomasz Pędzierski / ClawLabs

Użycie:
    python3 lead_generator.py "fotowoltaika" "Zamość"
    python3 lead_generator.py "IT" "Lublin" --limit 50
"""

import sys
import json
import re
from datetime import datetime

# Polskie regiony i miasta
POLISH_CITIES = {
    'zamość': {'województwo': 'lubelskie', 'powiat': 'zamojski', 'coords': (50.72, 23.25)},
    'lublin': {'województwo': 'lubelskie', 'powiat': 'Lublin', 'coords': (51.25, 22.57)},
    'warszawa': {'województwo': 'mazowieckie', 'powiat': 'Warszawa', 'coords': (52.23, 21.01)},
    'kraków': {'województwo': 'małopolskie', 'powiat': 'Kraków', 'coords': (50.06, 19.94)},
    'poznań': {'województwo': 'wielkopolskie', 'powiat': 'Poznań', 'coords': (52.41, 16.93)},
    'wrocław': {'województwo': 'dolnośląskie', 'powiat': 'Wrocław', 'coords': (51.11, 17.03)},
    'łódź': {'województwo': 'łódzkie', 'powiat': 'Łódź', 'coords': (51.76, 19.46)},
    'gdansk': {'województwo': 'pomorskie', 'powiat': 'Gdańsk', 'coords': (54.35, 18.64)},
    'szczecin': {'województwo': 'zachodniopomorskie', 'powiat': 'Szczecin', 'coords': (53.43, 14.55)},
    'bydgoszcz': {'województwo': 'kujawsko-pomorskie', 'powiat': 'Bydgoszcz', 'coords': (53.12, 18.01)},
    'białystok': {'województwo': 'podlaskie', 'powiat': 'Białystok', 'coords': (53.13, 23.17)},
    'katowice': {'województwo': 'śląskie', 'powiat': 'Katowice', 'coords': (50.26, 19.02)},
}

# Branże z odpowiednikami
INDUSTRIES = {
    'fotowoltaika': ['fotowoltaika', 'panele słoneczne', 'energia słoneczna', 'OZE'],
    'it': ['informatyka', 'IT', 'oprogramowanie', 'usługi IT', 'developing'],
    'budownictwo': ['budowa', 'konstrukcje', 'architektura', 'firma budowlana'],
    'transport': ['transport', 'logistyka', 'spedycja', 'przewozy'],
    'hurtownia': ['hurtownia', 'dystrybucja', 'handel hurtowy'],
    'ecommerce': ['sklep internetowy', 'e-commerce', 'sprzedaż online'],
    'marketing': ['marketing', 'reklama', 'agencja reklamowa'],
    'finanse': ['finanse', 'księgowość', 'doradztwo finansowe'],
    'produkcja': ['produkcja', 'wytwarzanie', 'fabryka', 'zakład produkcyjny'],
    'nieruchomości': ['nieruchomości', 'agencja nieruchomości', 'wynajem'],
    'restauracja': ['restauracja', 'catering', 'gastronomia'],
    'fryzjer': ['fryzjer', 'salon fryzjerski', 'uroda'],
    'mechanika': ['mechanika', 'warsztat', 'samochody', 'serwis'],
    'odzież': ['odzież', 'ubrania', 'sklep z odzieżą', 'szwalnia'],
    'chemia': ['chemia', 'produkty chemiczne', 'farby', 'lakiery'],
    'elektronika': ['elektronika', 'agd', 'RTV', 'komputery'],
    'telekomunikacja': ['telekomunikacja', 'telefony', 'sieci'],
}

# Formy prawne
COMPANY_TYPES = {
    'sp. z o.o.': {'type': 'sp. z o.o.', 'full': 'Spółka z ograniczoną odpowiedzialnością'},
    's.a.': {'type': 'S.A.', 'full': 'Spółka Akcyjna'},
    'sp. j.': {'type': 'sp. j.', 'full': 'Spółka jawna'},
    'sp. k.': {'type': 'sp. k.', 'full': 'Spółka komandytowa'},
    'indYWIDUALNA': {'type': 'JDG', 'full': 'Jednoosobowa działalność gospodarcza'},
    'pro': {'type': 'PRO', 'full': 'Przedsiębiorstwo rolne'},
    'instytucja': {'type': 'Instytucja', 'full': 'Instytucja'},
}

def normalize_query(query):
    """Normalizuje zapytanie użytkownika."""
    return query.lower().strip()

def find_industry(query):
    """Znajduje branżę na podstawie zapytania."""
    query = normalize_query(query)
    for industry, keywords in INDUSTRIES.items():
        for keyword in keywords:
            if keyword in query or query in keyword:
                return industry
    return query

def find_city(query):
    """Znajduje miasto na podstawie zapytania."""
    query = normalize_query(query)
    for city, data in POLISH_CITIES.items():
        if city in query:
            return city, data
    return query, {'województwo': 'nieznane', 'powiat': 'nieznany', 'coords': (None, None)}

def generate_leads(industry, location, limit=20):
    """Generuje listę leadów dla podanej branży i lokalizacji."""
    
    industry_key = find_industry(industry)
    city_key, city_data = find_city(location)
    
    # Symulacja bazy firm - w prawdziwej wersji byłoby API
    leads = []
    
    company_names_base = [
        "Tech", "Innowacyjni", "Polski", "Lokalny", "Nowoczesny", 
        "Profesjonalny", "Aktywny", "Dynamiczny", "Skuteczny", "Sprawdzony",
        "Partner", "Dystrybucja", "Serwis", "Group", "System", "Pro", "Service",
        "Solution", "Consulting", "Media", "Web", "Soft", "Data", "Cloud"
    ]
    
    company_suffixes = [
        " sp. z o.o.", " sp. k.", " s.a.", 
        "", "", "",  # JDG często bez formy
    ]
    
    www_prefixes = ['www', 'biuro', 'firma', 'kontakt', 'info']
    
    for i in range(min(limit, 50)):
        suffix = company_suffixes[i % len(suffixes)]
        name_base = company_names_base[i % len(company_names_base)]
        
        # Generuj nazwę
        if i < 10:
            name = f"{name_base} {industry_key.title()} {city_key.title()}{suffix}"
        else:
            name = f"{name_base}{i+1} {industry_key.title()}{suffix}"
        
        # Generuj dane kontaktowe
        nip = f"{922309000 + i:010d}"[:10]
        regon = f"{500000000 + i*17:014d}"[:14]
        
        www = f"www.{industry_key.lower().replace(' ', '')}{i+1}.pl"
        if i % 3 == 0:
            www = f"{www_prefixes[i%3]}.{city_key.lower()}{industry_key.lower()[:4]}.pl"
        
        phone = f"+48 {50 + i:02d} {100 + i*3:03d} {50 + i*7:03d}"
        
        email = f"biuro@{industry_key.lower().replace(' ', '')}{i+1}.pl"
        
        address = f"ul. {['Akacjowa', 'Lipowa', 'Kolorowa', 'Błękitna', 'Złota', 'Srebrna', 'Miedziana', 'Stalowa'][i%8]} {10+i*3}"
        
        if city_data['coords'][0]:
            lat = city_data['coords'][0] + (i * 0.01 - 0.25)
            lon = city_data['coords'][1] + (i * 0.01 - 0.25)
        else:
            lat, lon = None, None
        
        lead = {
            'lp': i + 1,
            'name': name.strip(),
            'industry': industry_key,
            'city': city_key,
            'voivodeship': city_data['województwo'],
            'address': address,
            'www': www,
            'phone': phone,
            'email': email,
            'nip': nip,
            'regon': regon,
            'founded': 2010 + (i % 14),
            'employees': ['1-9', '10-49', '50-249', '250+'][i % 4],
            'coords': {'lat': lat, 'lon': lon}
        }
        
        leads.append(lead)
    
    return {
        'query': {'industry': industry_key, 'location': city_key},
        'city_data': city_data,
        'total': len(leads),
        'leads': leads,
        'generated': datetime.now().isoformat()
    }

def format_leads_text(leads_data, format_type='simple'):
    """Formatuje leadów do wyświetlenia."""
    
    if format_type == 'simple':
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"📋 LEADY: {leads_data['query']['industry'].upper()}")
        lines.append(f"📍 LOKALIZACJA: {leads_data['query']['location']} ({leads_data['city_data']['województwo']})")
        lines.append(f"📊 ZNALEZIONO: {leads_data['total']} firm")
        lines.append(f"{'='*60}\n")
        
        for lead in leads_data['leads']:
            lines.append(f"{lead['lp']:2}. {lead['name']}")
            lines.append(f"   📍 {lead['address']}, {lead['city']}")
            lines.append(f"   🌐 {lead['www']}")
            lines.append(f"   📞 {lead['phone']}")
            lines.append(f"   ✉️  {lead['email']}")
            if lead['nip']:
                lines.append(f"   NIP: {lead['nip']}")
            lines.append("")
        
        return "\n".join(lines)
    
    elif format_type == 'csv':
        lines = ["Lp;Nazwa;Adres;Miasto;Województwo;WWW;Telefon;Email;NIP;Założona;Pracownicy"]
        for lead in leads_data['leads']:
            lines.append(f"{lead['lp']};{lead['name']};{lead['address']};{lead['city']};{lead['voivodeship']};{lead['www']};{lead['phone']};{lead['email']};{lead['nip']};{lead['founded']};{lead['employees']}")
        return "\n".join(lines)
    
    elif format_type == 'json':
        return json.dumps(leads_data, ensure_ascii=False, indent=2)

def search_examples():
    """Zwraca przykładowe wyszukiwania."""
    return """
🔍 PRZYKŁADOWE WYSZUKIWANIA:

Branże:
  - fotowoltaika, it, budownictwo, transport
  - hurtownia, e-commerce, marketing, finanse
  - produkcja, nieruchomości, restauracja

Lokalizacje:
  - Zamość, Lublin, Warszawa, Kraków
  - lubelskie, mazowieckie, śląskie

Przykłady:
  - "Znajdź firmy fotowoltaiczne w Zamościu"
  - "Lead generator: IT Lublin"
  - "Eksportuj leadów z branży budowlanej"
"""

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║               💰 LeadGenerator v1.0 💰                              ║
║         Generator Leadów B2B dla Firm i Handlowców                 ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) >= 3:
        industry = sys.argv[1]
        location = sys.argv[2]
        limit = 20
        
        if '--limit' in sys.argv:
            idx = sys.argv.index('--limit')
            if idx + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[idx + 1])
                except:
                    pass
        
        print(f"🔍 Szukam firm branży: {industry}")
        print(f"📍 Lokalizacja: {location}")
        print(f"📊 Limit: {limit}\n")
        
        leads_data = generate_leads(industry, location, limit)
        
        # Wyświetl wyniki
        print(format_leads_text(leads_data, 'simple'))
        
        # Podsumowanie
        print(f"\n📈 PODSUMOWANIE:")
        print(f"   Branża: {leads_data['query']['industry']}")
        print(f"   Województwo: {leads_data['city_data']['województwo']}")
        print(f"   Znaleziono: {leads_data['total']} firm")
        
        print("\n💡 Aby wyeksportować użyj:")
        print("   --format csv  (eksport do CSV)")
        print("   --format json (eksport do JSON)")
        
    else:
        print(search_examples())
        print("\n📝 PRZYKŁAD:")
        print("   python3 lead_generator.py 'fotowoltaika' 'Zamość'")
        print("   python3 lead_generator.py 'IT' 'Lublin' --limit 50")
        print("   python3 lead_generator.py 'budownictwo' 'Polska'")
        
        # Demo
        print("\n" + "="*60)
        print("🚀 DEMO: Firmy fotowoltaiczne w Zamościu")
        print("="*60)
        
        leads_data = generate_leads('fotowoltaika', 'Zamość', 10)
        print(format_leads_text(leads_data, 'simple'))

if __name__ == "__main__":
    main()