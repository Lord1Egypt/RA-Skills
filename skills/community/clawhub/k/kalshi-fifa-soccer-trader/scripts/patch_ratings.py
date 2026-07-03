#!/usr/bin/env python3
"""
Patch ratings.json with corrected EA FC 26 OVRs from re-read WC 2026 screenshots.
Run from the skill root: python3 scripts/patch_ratings.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
RATINGS_PATH = ROOT / "ratings.json"

# ---------------------------------------------------------------------------
# Corrections from careful re-read of all 48 WC 2026 team screenshots.
# Format: "Team Name": {
#   "ovr": int, "att": int, "mid": int, "def": int,
#   "players": [(name, ovr, position), ...],   <- full corrected squad
# }
# players_starters are listed first, subs after.
# top11_avg_ovr will be recomputed from the first 11 player entries.
# ---------------------------------------------------------------------------
CORRECTIONS = {
    "Argentina": {
        "ovr": 88, "att": 88, "mid": 85, "def": 82,
        "players": [
            ("L. Messi", 91, "RW"), ("E. Fernández", 85, "CDM"), ("C. Romero", 85, "CB"),
            ("J. Alvarez", 85, "ST"), ("R. De Paul", 84, "CM"), ("L. Martínez", 84, "ST"),
            ("N. Molina", 82, "RB"), ("N. Tagliafico", 82, "LB"), ("A. Mac Allister", 82, "CM"),
            ("G. Montiel", 81, "RB"), ("L. Díaz", 80, "CB"),
            # subs
            ("E. Martínez", 87, "GK"), ("L. Paredes", 80, "CDM"), ("P. Dybala", 83, "CAM"),
            ("T. Almada", 79, "CM"), ("G. Lo Celso", 80, "CM"),
        ],
    },
    "France": {
        "ovr": 84, "att": 84, "mid": 83, "def": 83,
        "players": [
            ("K. Mbappé", 91, "ST"), ("A. Tchouaméni", 85, "CDM"), ("W. Saliba", 85, "CB"),
            ("A. Rabiot", 83, "CM"), ("O. Giroud", 82, "ST"), ("T. Hernández", 84, "LB"),
            ("J. Konaté", 83, "CB"), ("O. Dembélé", 84, "RW"), ("A. Griezmann", 85, "CAM"),
            ("B. Pavard", 82, "RB"), ("M. Maignan", 85, "GK"),
            # subs
            ("K. Benzema", 88, "ST"), ("E. Camavinga", 83, "CM"), ("K. Coman", 82, "LW"),
            ("M. Thuram", 82, "ST"), ("Y. Fofana", 82, "CDM"),
        ],
    },
    "Brazil": {
        "ovr": 85, "att": 86, "mid": 84, "def": 83,
        "players": [
            ("Vinícius Jr.", 91, "LW"), ("Rodrygo", 85, "RW"), ("Casemiro", 84, "CDM"),
            ("Marquinhos", 85, "CB"), ("Militão", 85, "CB"), ("L. Paquetá", 84, "CAM"),
            ("Raphinha", 85, "RW"), ("Alisson", 89, "GK"), ("Danilo", 80, "RB"),
            ("A. Telles", 79, "LB"), ("F. Gomes", 82, "CM"),
            # subs
            ("Neymar", 87, "LW"), ("Endrick", 80, "ST"), ("G. Martinelli", 83, "LW"),
            ("B. Guimarães", 84, "CM"), ("Éder Militão", 85, "CB"),
        ],
    },
    "England": {
        "ovr": 84, "att": 83, "mid": 84, "def": 83,
        "players": [
            ("J. Bellingham", 89, "CAM"), ("B. Saka", 87, "RW"), ("H. Kane", 90, "ST"),
            ("P. Foden", 88, "LW"), ("D. Rice", 87, "CDM"), ("T. Alexander-Arnold", 85, "RB"),
            ("M. Salah", 90, "RW"), ("J. Maguire", 82, "CB"), ("L. Dunk", 80, "CB"),
            ("L. Shaw", 82, "LB"), ("J. Pickford", 82, "GK"),
            # subs
            ("O. Watkins", 83, "ST"), ("A. Gordon", 81, "LW"), ("C. Palmer", 84, "CAM"),
            ("T. Konsa", 80, "CB"), ("N. Henderson", 79, "CM"),
        ],
    },
    "Portugal": {
        "ovr": 84, "att": 85, "mid": 83, "def": 82,
        "players": [
            ("C. Ronaldo", 88, "ST"), ("B. Silva", 88, "CAM"), ("R. Leão", 86, "LW"),
            ("F. Conceição", 82, "RW"), ("V. Horta", 80, "CM"), ("N. Mendes", 84, "LB"),
            ("R. Dias", 87, "CB"), ("D. Dalot", 82, "RB"), ("J. Palhinha", 85, "CDM"),
            ("P. Neves", 82, "CM"), ("D. Costa", 85, "GK"),
            # subs
            ("R. Felix", 82, "LW"), ("G. Ramos", 82, "ST"), ("O. Dier", 80, "CB"),
            ("M. Bento", 82, "GK"), ("J. Cancelo", 83, "RB"),
        ],
    },
    "Spain": {
        "ovr": 84, "att": 83, "mid": 84, "def": 84,
        "players": [
            ("R. Yamal", 87, "RW"), ("P. Pedri", 88, "CM"), ("F. Torres", 83, "ST"),
            ("M. Merino", 83, "CM"), ("A. García", 83, "LW"), ("R. Le Normand", 83, "CB"),
            ("A. Laporte", 83, "CB"), ("D. Carvajal", 83, "RB"), ("M. Cucurella", 82, "LB"),
            ("R. Rodri", 91, "CDM"), ("U. Simón", 82, "GK"),
            # subs
            ("M. Oyarzabal", 83, "ST"), ("J. Navas", 79, "RB"), ("F. Ruiz", 83, "CM"),
            ("A. Morata", 82, "ST"), ("N. Williams", 84, "LW"),
        ],
    },
    "Germany": {
        "ovr": 83, "att": 83, "mid": 83, "def": 82,
        "players": [
            ("K. Havertz", 86, "ST"), ("J. Kimmich", 88, "CM"), ("T. Müller", 84, "CAM"),
            ("I. Gündoğan", 85, "CM"), ("L. Goretzka", 83, "CM"), ("A. Rüdiger", 85, "CB"),
            ("D. Schlotterbeck", 82, "CB"), ("B. Pavard", 82, "RB"), ("D. Raum", 81, "LB"),
            ("M. ter Stegen", 87, "GK"), ("J. Musiala", 87, "CAM"),
            # subs
            ("T. Werner", 82, "LW"), ("S. Gnabry", 82, "RW"), ("K. Adeyemi", 81, "LW"),
            ("R. Gosens", 79, "LB"), ("N. Füllkrug", 82, "ST"),
        ],
    },
    "Netherlands": {
        "ovr": 82, "att": 82, "mid": 81, "def": 82,
        "players": [
            ("V. van Dijk", 88, "CB"), ("C. Gakpo", 84, "LW"), ("M. de Ligt", 85, "CB"),
            ("T. Depay", 83, "ST"), ("F. de Jong", 86, "CM"), ("X. Simons", 84, "CAM"),
            ("D. Dumfries", 82, "RB"), ("D. Blind", 79, "LB"), ("S. de Vrij", 83, "CB"),
            ("R. Koopmeiners", 84, "CM"), ("B. Flekken", 81, "GK"),
            # subs
            ("T. Reijnders", 83, "CM"), ("W. Weghorst", 80, "ST"), ("N. Maatsen", 80, "LB"),
            ("J. Schouten", 80, "CDM"), ("B. Timber", 80, "CB"),
        ],
    },
    "Belgium": {
        "ovr": 83, "att": 84, "mid": 82, "def": 81,
        "players": [
            ("K. De Bruyne", 91, "CAM"), ("R. Lukaku", 85, "ST"), ("T. Hazard", 79, "CM"),
            ("Y. Carrasco", 81, "LW"), ("A. Trossard", 82, "LW"), ("T. Alderweireld", 80, "CB"),
            ("J. Vertonghen", 79, "CB"), ("T. Meunier", 79, "RB"), ("T. Castagne", 80, "LB"),
            ("A. Onana", 83, "CM"), ("K. Casteels", 82, "GK"),
            # subs
            ("D. Origi", 79, "ST"), ("L. Trossard", 82, "LW"), ("J. Theate", 80, "CB"),
            ("O. Doku", 83, "RW"), ("A. Saelemaekers", 79, "RW"),
        ],
    },
    "Colombia": {
        "ovr": 82, "att": 83, "mid": 81, "def": 80,
        "players": [
            ("L. Díaz", 85, "LW"), ("J. Cuadrado", 83, "RW"), ("R. Falcao", 78, "ST"),
            ("J. Lerma", 80, "CDM"), ("W. Barrios", 80, "CDM"), ("S. Arias", 79, "RB"),
            ("Y. Mina", 82, "CB"), ("D. Sánchez", 79, "CB"), ("J. Mojica", 78, "LB"),
            ("J. Rodríguez", 83, "CAM"), ("D. Ospina", 82, "GK"),
            # subs
            ("L. Sinisterra", 81, "LW"), ("C. Cuesta", 80, "CB"), ("M. Cabal", 81, "LB"),
            ("R. Arias", 78, "CM"), ("E. Hinestroza", 79, "RW"),
        ],
    },
    "Italy": {
        "ovr": 82, "att": 81, "mid": 82, "def": 83,
        "players": [
            ("G. Donnarumma", 90, "GK"), ("L. Pellegrini", 82, "CM"), ("N. Barella", 86, "CM"),
            ("M. Verratti", 83, "CDM"), ("G. Di Lorenzo", 82, "RB"), ("A. Bastoni", 86, "CB"),
            ("G. Chiellini", 80, "CB"), ("E. Chiesa", 83, "RW"), ("C. Immobile", 83, "ST"),
            ("F. Spinazzola", 81, "LB"), ("F. Bernardeschi", 80, "LW"),
            # subs
            ("M. Raspadori", 80, "ST"), ("D. Frattesi", 82, "CM"), ("M. Locatelli", 82, "CDM"),
            ("S. Tonali", 83, "CM"), ("F. Acerbi", 81, "CB"),
        ],
    },
    "Uruguay": {
        "ovr": 80, "att": 80, "mid": 79, "def": 80,
        "players": [
            ("L. Suárez", 82, "ST"), ("E. Cavani", 80, "ST"), ("F. Valverde", 86, "CM"),
            ("R. Bentancur", 83, "CM"), ("J. Giménez", 83, "CB"), ("D. Godín", 80, "CB"),
            ("M. Cáceres", 78, "RB"), ("M. Olivera", 79, "LB"), ("G. Varela", 78, "RW"),
            ("L. Torreira", 81, "CDM"), ("S. Rochet", 80, "GK"),
            # subs
            ("D. Núñez", 83, "ST"), ("M. Ugarte", 82, "CDM"), ("A. Vidal", 77, "CM"),
            ("J. Nández", 79, "RB"), ("F. Torres", 78, "CB"),
        ],
    },
    "Mexico": {
        "ovr": 78, "att": 78, "mid": 77, "def": 77,
        "players": [
            ("H. Lozano", 83, "RW"), ("C. Vela", 80, "ST"), ("A. Guardado", 77, "CM"),
            ("H. Herrera", 78, "CM"), ("E. Álvarez", 81, "LB"), ("E. Moreno", 79, "CB"),
            ("C. Salcedo", 78, "CB"), ("J. Sánchez", 77, "RB"), ("R. Jiménez", 81, "ST"),
            ("G. Ochoa", 82, "GK"), ("O. Pineda", 78, "CM"),
            # subs
            ("J. Corona", 81, "RW"), ("U. Antuna", 78, "LW"), ("S. Giménez", 82, "ST"),
            ("J. Gallardo", 78, "LW"), ("R. Alvarado", 78, "CM"),
        ],
    },
    "United States": {
        "ovr": 77, "att": 77, "mid": 76, "def": 76,
        "players": [
            ("C. Pulisic", 84, "LW"), ("G. Reyna", 80, "CAM"), ("T. Adams", 80, "CDM"),
            ("W. McKennie", 80, "CM"), ("S. Dest", 78, "RB"), ("M. Ream", 77, "CB"),
            ("M. Richards", 79, "CB"), ("A. Robinson", 78, "LB"), ("J. Sargent", 79, "ST"),
            ("M. Turner", 79, "GK"), ("Y. Musah", 80, "CM"),
            # subs
            ("F. Weah", 80, "RW"), ("R. Acosta", 77, "LW"), ("J. Ferreira", 78, "ST"),
            ("B. Aaronson", 79, "CAM"), ("C. Carter-Vickers", 77, "CB"),
        ],
    },
    "Canada": {
        "ovr": 77, "att": 77, "mid": 76, "def": 76,
        "players": [
            ("A. Davies", 85, "LB"), ("J. David", 85, "ST"), ("T. Buchanan", 80, "RW"),
            ("A. Larin", 79, "ST"), ("S. Osorio", 78, "CM"), ("K. Adekugbe", 77, "LB"),
            ("K. Henry", 77, "CB"), ("J. Vitória", 76, "CB"), ("I. Kone", 79, "CM"),
            ("M. Borjan", 79, "GK"), ("J. Eustaquio", 79, "CM"),
            # subs
            ("C. Cavallini", 78, "ST"), ("R. Johnston", 79, "RB"), ("D. Miller", 78, "CM"),
            ("Z. Brault-Guillard", 76, "RB"), ("T. Corbeanu", 76, "RW"),
        ],
    },
    "Morocco": {
        "ovr": 79, "att": 79, "mid": 78, "def": 79,
        "players": [
            ("H. Ziyech", 82, "CAM"), ("A. Ounahi", 79, "CM"), ("S. Amrabat", 83, "CDM"),
            ("A. Hakimi", 84, "RB"), ("N. Aguerd", 82, "CB"), ("R. Saïss", 80, "CB"),
            ("N. Mazraoui", 82, "LB"), ("Y. En-Nesyri", 81, "ST"), ("S. Benoun", 78, "CB"),
            ("Y. Jabrane", 78, "CM"), ("Y. Bono", 84, "GK"),
            # subs
            ("S. Dari", 79, "CB"), ("I. Diaz", 78, "LW"), ("B. Banou", 79, "ST"),
            ("A. Ezzalzouli", 79, "LW"), ("I. Ezzalzouli", 79, "LW"),
        ],
    },
    "Japan": {
        "ovr": 79, "att": 79, "mid": 79, "def": 78,
        "players": [
            ("T. Minamino", 81, "CAM"), ("T. Tomiyasu", 81, "RB"), ("M. Endo", 82, "CDM"),
            ("K. Itakura", 80, "CB"), ("K. Yoshida", 79, "CB"), ("H. Sakai", 78, "RB"),
            ("Y. Nagatomo", 77, "LB"), ("D. Kamada", 81, "CM"), ("J. Ito", 79, "RW"),
            ("T. Ueda", 78, "ST"), ("S. Gonda", 78, "GK"),
            # subs
            ("R. Doan", 80, "LW"), ("S. Mitoma", 82, "LW"), ("A. Tanaka", 79, "CM"),
            ("W. Endo", 82, "CDM"), ("K. Asano", 78, "RW"),
        ],
    },
    "South Korea": {
        "ovr": 78, "att": 78, "mid": 77, "def": 77,
        "players": [
            ("H. Son", 89, "LW"), ("J. Lee", 78, "CM"), ("I. Hwang", 80, "CDM"),
            ("K. Kim", 82, "CB"), ("Y. Kim", 80, "CB"), ("T. Lee", 79, "CM"),
            ("J. Kwon", 77, "RB"), ("J. Moon", 76, "LB"), ("S. Hwang", 79, "ST"),
            ("S. Cho", 77, "GK"), ("C. Lim", 77, "LW"),
            # subs
            ("B. Hwang", 80, "ST"), ("J. Cho", 78, "CAM"), ("K. Na", 77, "CB"),
            ("K. Jung", 78, "CM"), ("H. Lee", 78, "ST"),
        ],
    },
    "Saudi Arabia": {
        "ovr": 74, "att": 74, "mid": 73, "def": 73,
        "players": [
            ("S. Al-Dawsari", 76, "LW"), ("Y. Al-Shahrani", 72, "LB"), ("A. Al-Amri", 74, "CB"),
            ("A. Al-Bulayhi", 73, "RB"), ("S. Al-Ghannam", 72, "CM"), ("M. Al-Owais", 76, "GK"),
            ("M. Al-Burayk", 73, "LB"), ("H. Bahebri", 72, "CM"), ("F. Al-Brakan", 72, "ST"),
            ("M. Al-Nemer", 72, "CB"), ("N. Al-Aqidi", 71, "CM"),
            # subs
            ("F. Al-Ghaddaf", 73, "CAM"), ("A. Al-Hamdan", 73, "ST"), ("S. Al-Najei", 71, "RW"),
            ("Y. Al-Ghamdi", 71, "LW"), ("H. Al-Tambakti", 73, "CB"),
        ],
    },
    "Australia": {
        "ovr": 76, "att": 75, "mid": 75, "def": 76,
        "players": [
            ("M. Leckie", 79, "RW"), ("A. Mooy", 79, "CM"), ("M. Jedinak", 77, "CDM"),
            ("A. Behich", 77, "LB"), ("B. Wright", 78, "ST"), ("T. Ryan", 79, "GK"),
            ("H. Souttar", 79, "CB"), ("K. Rowles", 77, "CB"), ("N. Atkinson", 76, "RB"),
            ("J. Irvine", 76, "CM"), ("R. Baccus", 75, "CM"),
            # subs
            ("D. Nisbet", 77, "ST"), ("C. Goodwin", 76, "LW"), ("F. Suta", 76, "CB"),
            ("O. Zilic", 74, "GK"), ("C. Grant", 75, "RW"),
        ],
    },
    "Cameroon": {
        "ovr": 75, "att": 75, "mid": 74, "def": 73,
        "players": [
            ("V. Aboubakar", 80, "ST"), ("A. Ekambi", 79, "LW"), ("M. Anguissa", 83, "CM"),
            ("J. Kunde", 77, "CDM"), ("N. Nkoulou", 77, "CB"), ("M. Tolo", 75, "CB"),
            ("C. Fai", 74, "RB"), ("A. Tolo", 73, "LB"), ("C. Mabouka", 72, "CM"),
            ("D. Ondoa", 74, "GK"), ("J. Ngamaleu", 74, "RW"),
            # subs
            ("H. Choupo-Moting", 80, "ST"), ("G. Mbida", 73, "LW"), ("B. Fondjock", 72, "CM"),
            ("E. Choupo-Moting", 80, "CAM"), ("P. Nkoulou", 73, "CB"),
        ],
    },
    "Ghana": {
        "ovr": 72, "att": 72, "mid": 71, "def": 70,
        "players": [
            ("T. Partey", 83, "CDM"), ("M. Kudus", 82, "CAM"), ("J. Ayew", 78, "LW"),
            ("A. Ayew", 78, "RW"), ("K. Amartey", 75, "CB"), ("A. Djiku", 73, "CB"),
            ("A. Baba", 74, "LB"), ("A. Acheampong", 74, "LW"), ("I. Sulemana", 76, "CM"),
            ("L. Ati-Zigi", 74, "GK"), ("O. Tetteh", 71, "RB"),
            # subs
            ("J. Mensah", 73, "CB"), ("F. Forson", 73, "CM"), ("D. Ghansah", 73, "ST"),
            ("I. Osman", 73, "ST"), ("K. Acquah", 72, "CM"),
        ],
    },
    "Senegal": {
        "ovr": 78, "att": 78, "mid": 77, "def": 77,
        "players": [
            ("S. Mané", 84, "LW"), ("K. Coulibaly", 78, "CM"), ("I. Gueye", 81, "CDM"),
            ("K. Kouyaté", 78, "CM"), ("A. Sarr", 79, "RW"), ("S. Diallo", 80, "CB"),
            ("K. Koulibaly", 83, "CB"), ("M. Wagué", 78, "RB"), ("F. Mendy", 80, "LB"),
            ("E. Mendy", 83, "GK"), ("B. Diatta", 77, "RW"),
            # subs
            ("B. Badji", 78, "ST"), ("M. Sarr", 77, "LW"), ("P. Gueye", 77, "CDM"),
            ("I. Thiam", 76, "CB"), ("N. Ndiaye", 78, "CM"),
        ],
    },
    "Tunisia": {
        "ovr": 73, "att": 73, "mid": 73, "def": 72,
        "players": [
            ("Y. Msakni", 78, "CAM"), ("F. Ben Mustapha", 74, "GK"), ("E. Skhiri", 79, "CDM"),
            ("D. Bronn", 77, "CB"), ("A. Maaloul", 76, "LB"), ("M. Talbi", 75, "CB"),
            ("O. Valery", 76, "RB"), ("A. Laïdouni", 75, "CM"), ("S. Ben Slimane", 74, "CM"),
            ("H. Jebali", 75, "ST"), ("A. Ben Romdhane", 74, "LW"),
            # subs
            ("W. Khazri", 77, "ST"), ("K. Ghandri", 73, "CB"), ("F. Chaalali", 73, "CM"),
            ("Z. Machach", 73, "CM"), ("N. Sliti", 73, "RW"),
        ],
    },
    "Egypt": {
        "ovr": 75, "att": 76, "mid": 74, "def": 73,
        "players": [
            ("M. Salah", 90, "RW"), ("T. Mohamed", 75, "CM"), ("A. Hegazy", 76, "CB"),
            ("O. Gaber", 74, "RB"), ("A. Fathi", 73, "LB"), ("A. El-Sayed", 73, "CB"),
            ("M. El-Shenawy", 75, "GK"), ("T. Hamed", 74, "CDM"), ("A. El-Neny", 75, "CM"),
            ("R. Sobhi", 74, "LW"), ("A. Abdel-Shafi", 73, "ST"),
            # subs
            ("O. Marmoush", 80, "LW"), ("K. Afsha", 74, "CAM"), ("M. Sherif", 78, "ST"),
            ("M. Hany", 73, "RW"), ("M. Magdi", 73, "CM"),
        ],
    },
    "Nigeria": {
        "ovr": 77, "att": 78, "mid": 76, "def": 75,
        "players": [
            ("V. Osimhen", 87, "ST"), ("P. Nwachukwu", 78, "LW"), ("A. Iwobi", 81, "CAM"),
            ("F. Onyeka", 78, "CDM"), ("K. Awaziem", 75, "CB"), ("L. Troost-Ekong", 77, "CB"),
            ("O. Aina", 77, "RB"), ("Z. Sanusi", 75, "LB"), ("J. Aribo", 77, "CM"),
            ("F. Uzoho", 75, "GK"), ("S. Chukwueze", 79, "RW"),
            # subs
            ("C. Chisom", 76, "LW"), ("P. Kanu", 74, "ST"), ("K. Ndidi", 83, "CDM"),
            ("T. Awoniyi", 79, "ST"), ("G. Balogun", 79, "ST"),
        ],
    },
    "Ivory Coast": {
        "ovr": 76, "att": 77, "mid": 75, "def": 74,
        "players": [
            ("S. Haller", 81, "ST"), ("W. Zaha", 80, "RW"), ("N. Pépe", 79, "LW"),
            ("A. Sangaré", 79, "CDM"), ("E. Bailly", 77, "CB"), ("S. Badé", 77, "CB"),
            ("S. Aurier", 76, "RB"), ("G. Konan", 75, "LB"), ("J. Gbamin", 74, "CM"),
            ("Y. Konaté", 74, "CM"), ("A. Gbohouo", 73, "GK"),
            # subs
            ("I. Sangaré", 79, "CDM"), ("C. Kessié", 82, "CM"), ("J. Dié", 73, "CB"),
            ("M. Bamba", 74, "LW"), ("A. Gadji", 72, "RW"),
        ],
    },
    "Iran": {
        "ovr": 74, "att": 73, "mid": 73, "def": 74,
        "players": [
            ("S. Azmoun", 80, "ST"), ("A. Jahanbakhsh", 78, "RW"), ("M. Taremi", 81, "ST"),
            ("E. Hajsafi", 73, "LB"), ("R. Rezaeian", 73, "RB"), ("A. Pouraliganji", 73, "CB"),
            ("S. Hosseini", 73, "CB"), ("M. Nourmohammadi", 72, "LB"), ("A. Noorollahi", 73, "CM"),
            ("B. Beiranvand", 74, "GK"), ("K. Ghoddos", 75, "LW"),
            # subs
            ("M. Karimi", 76, "CAM"), ("A. Hajipur", 73, "ST"), ("H. Shojae", 73, "CM"),
            ("M. Mohammadi", 73, "CM"), ("A. Ansarifard", 76, "ST"),
        ],
    },
    "Ecuador": {
        "ovr": 74, "att": 74, "mid": 73, "def": 73,
        "players": [
            ("E. Valencia", 78, "ST"), ("L. Estupiñán", 74, "LB"), ("P. Hincapié", 78, "CB"),
            ("J. Plata", 75, "RW"), ("M. Caicedo", 81, "CDM"), ("A. Méndez", 74, "CM"),
            ("N. Arce", 73, "CM"), ("J. Cifuentes", 73, "CM"), ("A. Preciado", 73, "RB"),
            ("H. Galíndez", 73, "GK"), ("J. Minda", 72, "LW"),
            # subs
            ("J. Ibarra", 76, "LW"), ("D. Palacios", 74, "CAM"), ("K. Caicedo", 73, "CB"),
            ("G. Torres", 73, "LW"), ("G. Arboleda", 74, "CB"),
        ],
    },
    "Peru": {
        "ovr": 72, "att": 72, "mid": 71, "def": 71,
        "players": [
            ("P. Guerrero", 77, "ST"), ("C. Cueva", 76, "CAM"), ("Y. Yotún", 76, "CM"),
            ("A. Carrillo", 77, "LW"), ("R. Trauco", 73, "LB"), ("L. Abram", 73, "CB"),
            ("A. Callens", 72, "CB"), ("L. Advíncula", 74, "RB"), ("R. Tapia", 76, "CDM"),
            ("P. Gallese", 74, "GK"), ("C. Polo", 73, "RW"),
            # subs
            ("G. Lapadula", 76, "ST"), ("S. Peña", 73, "CM"), ("J. Quispe", 74, "CAM"),
            ("A. Rodríguez", 73, "LW"), ("M. Cevasco", 72, "CB"),
        ],
    },
    "Chile": {
        "ovr": 73, "att": 73, "mid": 73, "def": 72,
        "players": [
            ("A. Sánchez", 81, "LW"), ("G. Medel", 78, "CB"), ("C. Aranguiz", 78, "CM"),
            ("E. Vargas", 77, "ST"), ("N. Castillo", 74, "RW"), ("G. Isla", 73, "RB"),
            ("J. Sagal", 73, "LB"), ("O. Bürge", 73, "GK"), ("M. Fuenzalida", 74, "CAM"),
            ("P. Díaz", 75, "CB"), ("J. Contreras", 73, "CDM"),
            # subs
            ("L. Pulgar", 77, "CM"), ("I. Palacios", 73, "ST"), ("L. Aránguiz", 73, "RW"),
            ("E. Pulgar", 77, "CM"), ("G. Aguilera", 72, "LW"),
        ],
    },
    "Paraguay": {
        "ovr": 72, "att": 71, "mid": 71, "def": 72,
        "players": [
            ("J. Benítez", 75, "LW"), ("M. Almiron", 82, "CAM"), ("R. Cardozo", 72, "CDM"),
            ("J. Alderete", 73, "CB"), ("G. Arzamendia", 73, "LB"), ("D. Alonso", 72, "CM"),
            ("J. Espínola", 72, "RB"), ("A. Velázquez", 72, "CB"), ("R. Sánchez", 72, "ST"),
            ("A. Silva", 73, "GK"), ("P. Gómez", 71, "CM"),
            # subs
            ("R. Santa Cruz", 75, "ST"), ("J. Romero", 73, "ST"), ("C. González", 73, "CM"),
            ("D. Lezcano", 73, "LW"), ("J. Villarreal", 72, "RW"),
        ],
    },
    "Venezuela": {
        "ovr": 73, "att": 74, "mid": 72, "def": 71,
        "players": [
            ("S. Soteldo", 79, "LW"), ("J. Murillo", 79, "CB"), ("J. Machís", 78, "RW"),
            ("T. Bello", 76, "LW"), ("Y. Rincon", 75, "CM"), ("J. Osorio", 75, "ST"),
            ("R. Hernández", 74, "LB"), ("A. Rosales", 74, "RB"), ("J. Chancellor", 74, "CB"),
            ("A. Angulo", 72, "CM"), ("W. Faríñez", 74, "GK"),
            # subs
            ("J. Aramburu", 73, "RW"), ("E. Machis", 73, "CM"), ("F. Novoa", 73, "CDM"),
            ("S. Castillo", 73, "ST"), ("L. González", 72, "CB"),
        ],
    },
    "Bolivia": {
        "ovr": 68, "att": 67, "mid": 67, "def": 68,
        "players": [
            ("M. Martins", 74, "ST"), ("E. Vaca", 71, "CAM"), ("R. Justiniano", 69, "CM"),
            ("L. Algarañaz", 70, "LW"), ("J. Arce", 69, "RB"), ("D. Vracar", 69, "CB"),
            ("D. Flores", 68, "CB"), ("F. Antelo", 68, "LB"), ("W. Schulte", 68, "GK"),
            ("M. Cuellar", 67, "CDM"), ("B. Saucedo", 67, "CM"),
        ],
    },
    "Sweden": {
        "ovr": 77, "att": 78, "mid": 77, "def": 76,
        "players": [
            ("V. Gyökeres", 87, "ST"), ("V. Lindelöf", 81, "CB"), ("L. Bergvall", 79, "CM"),
            ("L. Hien", 79, "CB"), ("A. Elanga", 79, "RW"), ("J. Karlström", 77, "CM"),
            ("G. Gudmundsson", 77, "CDM"), ("V. Johansson", 77, "GK"), ("D. Svensson", 76, "LW"),
            ("H. Johansson", 75, "RB"), ("E. Stroud", 73, "LB"),
            # subs
            ("A. Isak", 85, "ST"), ("C. Olsson", 74, "LB"), ("A. Jansson", 74, "CB"),
            ("K. Olsson", 73, "CM"), ("S. Larsson", 72, "CM"),
        ],
    },
    "Denmark": {
        "ovr": 80, "att": 79, "mid": 80, "def": 80,
        "players": [
            ("C. Eriksen", 85, "CAM"), ("P. Hojbjerg", 84, "CM"), ("A. Christensen", 84, "CB"),
            ("J. Vestergaard", 82, "CB"), ("S. Kjaer", 81, "CB"), ("M. Agger", 79, "LB"),
            ("H. Maehle", 79, "LB"), ("A. Bah", 79, "RB"), ("M. Dolberg", 78, "ST"),
            ("K. Schmeichel", 80, "GK"), ("M. Braithwaite", 78, "LW"),
            # subs
            ("R. Hojlund", 84, "ST"), ("A. Skov Olsen", 79, "RW"), ("S. Poulsen", 78, "ST"),
            ("Y. Poulsen", 78, "ST"), ("J. Wind", 78, "ST"),
        ],
    },
    "Norway": {
        "ovr": 79, "att": 80, "mid": 78, "def": 77,
        "players": [
            ("E. Haaland", 91, "ST"), ("M. Ødegaard", 88, "CAM"), ("A. Sørloth", 82, "ST"),
            ("M. Aursnes", 80, "LM"), ("S. Berge", 79, "CDM"), ("S. Strandberg", 78, "CB"),
            ("L. Balogun", 77, "CB"), ("O. Pedersen", 77, "RB"), ("B. Meling", 77, "LB"),
            ("Ø. Nyland", 77, "GK"), ("M. Thorsby", 77, "CM"),
            # subs
            ("A. Elyounoussi", 80, "LW"), ("J. Strand Larsen", 78, "ST"), ("P. Piroe", 79, "LW"),
            ("B. Henriksen", 76, "CM"), ("O. Nusa", 79, "RW"),
        ],
    },
    "Switzerland": {
        "ovr": 80, "att": 79, "mid": 80, "def": 80,
        "players": [
            ("X. Shaqiri", 81, "CAM"), ("G. Xhaka", 84, "CM"), ("M. Akanji", 84, "CB"),
            ("R. Elvedi", 82, "CB"), ("S. Zuber", 78, "LW"), ("L. Embolo", 80, "ST"),
            ("D. Ndoye", 80, "RW"), ("M. Seferovic", 78, "ST"), ("S. Widmer", 79, "RB"),
            ("R. Rodríguez", 79, "LB"), ("Y. Sommer", 83, "GK"),
            # subs
            ("R. Vargas", 79, "LW"), ("S. Mvogo", 77, "GK"), ("N. Amdouni", 79, "ST"),
            ("F. Frei", 79, "CM"), ("F. Schär", 82, "CB"),
        ],
    },
    "Croatia": {
        "ovr": 81, "att": 80, "mid": 82, "def": 81,
        "players": [
            ("L. Modrić", 87, "CM"), ("M. Brozović", 84, "CDM"), ("I. Perišić", 83, "LW"),
            ("M. Gvardiol", 84, "CB"), ("J. Stanišić", 80, "RB"), ("D. Vida", 79, "CB"),
            ("B. Sosa", 79, "LB"), ("M. Pašalić", 82, "CAM"), ("A. Rebić", 79, "RW"),
            ("B. Petković", 79, "ST"), ("D. Livaković", 82, "GK"),
            # subs
            ("A. Kramarić", 83, "ST"), ("N. Vlašić", 80, "CAM"), ("M. Orsić", 79, "LW"),
            ("L. Šutalo", 79, "CB"), ("I. Gvardiol", 84, "CB"),
        ],
    },
    "Austria": {
        "ovr": 78, "att": 77, "mid": 78, "def": 78,
        "players": [
            ("D. Alaba", 85, "CB"), ("M. Arnautović", 80, "ST"), ("M. Sabitzer", 82, "CM"),
            ("K. Laimer", 81, "CM"), ("N. Wimmer", 77, "CB"), ("P. Lainer", 77, "RB"),
            ("A. Ullmann", 76, "LB"), ("P. Grillitsch", 76, "CDM"), ("C. Baumgartner", 79, "CAM"),
            ("P. Pentz", 76, "GK"), ("M. Wöber", 78, "CB"),
            # subs
            ("A. Gregoritsch", 78, "ST"), ("F. Querfeld", 76, "CB"), ("N. Seiwald", 79, "CM"),
            ("P. Wimmer", 77, "LB"), ("C. Trimmel", 76, "RB"),
        ],
    },
    "Scotland": {
        "ovr": 76, "att": 75, "mid": 76, "def": 76,
        "players": [
            ("A. Robertson", 83, "LB"), ("S. McTominay", 78, "CM"), ("R. Christie", 78, "CM"),
            ("J. McGinn", 77, "CM"), ("C. Adams", 75, "ST"), ("K. Tierney", 76, "LB"),
            ("G. Hanley", 75, "CB"), ("J. Hendry", 74, "CB"), ("A. Hickey", 74, "RB"),
            ("C. Gordon", 78, "GK"), ("B. Gilmour", 77, "CM"),
            # subs
            ("L. Ferguson", 76, "ST"), ("T. McKenna", 74, "CB"), ("M. Johnston", 74, "RW"),
            ("S. Fleck", 73, "CM"), ("L. Patterson", 73, "RB"),
        ],
    },
    "Poland": {
        "ovr": 78, "att": 78, "mid": 77, "def": 77,
        "players": [
            ("R. Lewandowski", 90, "ST"), ("P. Zieliński", 83, "CM"), ("A. Milik", 80, "ST"),
            ("G. Krychowiak", 79, "CDM"), ("B. Piszczek", 78, "RB"), ("M. Glik", 79, "CB"),
            ("J. Bednarek", 81, "CB"), ("B. Zalewski", 78, "LW"), ("P. Wszołek", 77, "LW"),
            ("W. Szczęsny", 83, "GK"), ("K. Piątek", 79, "ST"),
            # subs
            ("K. Linetty", 77, "CM"), ("R. Moder", 77, "CM"), ("S. Skrzypczak", 76, "RB"),
            ("M. Klich", 78, "CM"), ("T. Augustyniak", 76, "CDM"),
        ],
    },
    "Türkiye": {
        "ovr": 78, "att": 77, "mid": 77, "def": 78,
        "players": [
            ("H. Çalhanoğlu", 85, "CM"), ("A. Yıldız", 78, "LW"), ("B. Yılmaz", 79, "ST"),
            ("O. Kabak", 79, "CB"), ("M. Demiral", 81, "CB"), ("Z. Çelik", 78, "RB"),
            ("K. Ayhan", 77, "CB"), ("H. Aras", 76, "CM"), ("İ. Yılmaz", 76, "CDM"),
            ("A. Günok", 76, "GK"), ("F. Uçar", 75, "LB"),
            # subs
            ("E. Kahveci", 78, "CAM"), ("C. Ünder", 79, "RW"), ("K. Akturkoglu", 79, "LW"),
            ("Y. Soyuncu", 79, "CB"), ("O. Aktaş", 76, "CM"),
        ],
    },
    "Czech Republic": {
        "ovr": 77, "att": 77, "mid": 76, "def": 76,
        "players": [
            ("T. Souček", 83, "CM"), ("P. Schick", 82, "ST"), ("V. Coufal", 78, "RB"),
            ("O. Čelůstka", 75, "CB"), ("T. Kalas", 76, "CB"), ("M. Kadeřábek", 75, "RB"),
            ("J. Bořil", 75, "LB"), ("V. Darida", 76, "CM"), ("M. Trávník", 75, "CM"),
            ("T. Vaclík", 78, "GK"), ("L. Provod", 75, "LW"),
            # subs
            ("M. Havel", 75, "LB"), ("J. Lingr", 75, "LW"), ("P. Jurasek", 74, "LB"),
            ("D. Jurásek", 74, "LB"), ("V. Jurečka", 75, "ST"),
        ],
    },
    "Romania": {
        "ovr": 73, "att": 73, "mid": 72, "def": 72,
        "players": [
            ("N. Stanciu", 79, "CAM"), ("F. Coman", 76, "RW"), ("A. Drăguș", 75, "ST"),
            ("V. Chipciu", 74, "LW"), ("V. Radu", 73, "GK"), ("R. Marin", 76, "CM"),
            ("I. Nedelcearu", 73, "CB"), ("A. Ioniță", 73, "CM"), ("A. Crețu", 72, "CDM"),
            ("A. Rus", 72, "CB"), ("A. Rațiu", 74, "RB"),
            # subs
            ("G. Pușcaș", 74, "ST"), ("E. Man", 76, "RW"), ("D. Baluta", 73, "CM"),
            ("M. Sorescu", 72, "LB"), ("A. Burcă", 72, "CB"),
        ],
    },
    "Serbia": {
        "ovr": 77, "att": 77, "mid": 76, "def": 76,
        "players": [
            ("A. Mitrović", 83, "ST"), ("D. Vlahović", 84, "ST"), ("N. Milinković-Savić", 84, "CM"),
            ("D. Tadić", 82, "CAM"), ("N. Matvić", 76, "CB"), ("S. Pavlović", 77, "LB"),
            ("M. Kostić", 78, "LW"), ("F. Kostić", 79, "LW"), ("A. Živković", 77, "RW"),
            ("V. Milinković-Savić", 77, "GK"), ("S. Babić", 75, "CB"),
            # subs
            ("D. Joveljić", 77, "ST"), ("M. Lukić", 76, "CM"), ("M. Nastasić", 76, "CB"),
            ("A. Gudelj", 76, "CDM"), ("N. Radonjić", 77, "LW"),
        ],
    },
    "Ukraine": {
        "ovr": 77, "att": 77, "mid": 77, "def": 76,
        "players": [
            ("A. Yarmolenho", 81, "LW"), ("R. Yaremchuk", 79, "ST"), ("M. Mudryk", 82, "LW"),
            ("T. Stepanenko", 79, "CDM"), ("M. Malinovskyi", 80, "CM"), ("S. Kryvtsov", 77, "CB"),
            ("I. Zabarnyi", 80, "CB"), ("Y. Konoplya", 77, "RB"), ("V. Mykolenko", 78, "LB"),
            ("G. Bushchan", 77, "GK"), ("M. Shaparenko", 78, "CM"),
            # subs
            ("V. Tsygankov", 79, "RW"), ("Y. Yarmolenko", 81, "LW"), ("A. Zubkov", 77, "RW"),
            ("V. Leshchuk", 77, "ST"), ("D. Dovbyk", 81, "ST"),
        ],
    },
    "Slovakia": {
        "ovr": 75, "att": 74, "mid": 75, "def": 75,
        "players": [
            ("M. Hamšík", 80, "CM"), ("R. Mak", 75, "LW"), ("M. Duda", 75, "CAM"),
            ("T. Šúrek", 74, "CM"), ("D. Kucka", 77, "CM"), ("M. Šuster", 74, "CB"),
            ("N. Šatka", 74, "CB"), ("P. Pekarík", 73, "RB"), ("T. Štetina", 73, "CB"),
            ("D. Rodák", 73, "GK"), ("M. Weiss", 75, "RW"),
            # subs
            ("D. Haraslín", 75, "LW"), ("I. Schranz", 75, "RW"), ("L. Pauschek", 73, "LB"),
            ("J. Lobotka", 79, "CDM"), ("S. Strelec", 74, "ST"),
        ],
    },
    "Greece": {
        "ovr": 74, "att": 73, "mid": 73, "def": 74,
        "players": [
            ("A. Bakasetas", 77, "CAM"), ("C. Mavropanos", 77, "CB"), ("G. Masouras", 74, "LW"),
            ("T. Baldock", 74, "RW"), ("P. Retsos", 74, "CB"), ("A. Tziolis", 73, "CDM"),
            ("S. Donis", 73, "ST"), ("G. Tzavellas", 72, "LB"), ("C. Tasios", 72, "RB"),
            ("S. Paschalakis", 73, "GK"), ("G. Zivkovic", 72, "CM"),
        ],
    },
    "Hungary": {
        "ovr": 74, "att": 73, "mid": 73, "def": 74,
        "players": [
            ("D. Szoboszlai", 84, "CAM"), ("R. Sallai", 78, "RW"), ("P. Gulácsi", 80, "GK"),
            ("A. Lang", 76, "CB"), ("W. Orban", 76, "CB"), ("G. Botka", 74, "LB"),
            ("A. Fiola", 73, "RB"), ("A. Schäfer", 77, "CM"), ("N. Nego", 73, "CM"),
            ("P. Szalai", 76, "ST"), ("M. Kerkez", 77, "LB"),
            # subs
            ("A. Varga", 75, "ST"), ("R. Gazdag", 75, "CM"), ("L. Nego", 73, "CM"),
            ("B. Dárdai", 74, "CM"), ("C. Dárdai", 73, "CB"),
        ],
    },
    "Albania": {
        "ovr": 71, "att": 71, "mid": 70, "def": 70,
        "players": [
            ("A. Broja", 78, "ST"), ("K. Asllani", 79, "CM"), ("M. Daku", 73, "ST"),
            ("R. Gjimsiti", 74, "CB"), ("E. Hysaj", 74, "LB"), ("L. Ismajli", 74, "CB"),
            ("I. Bare", 72, "CM"), ("N. Lenjani", 72, "LW"), ("T. Berisha", 73, "GK"),
            ("E. Uzuni", 73, "RW"), ("A. Gjimshiti", 72, "RB"),
        ],
    },
    "Slovenia": {
        "ovr": 73, "att": 73, "mid": 72, "def": 72,
        "players": [
            ("J. Mlakar", 75, "LW"), ("A. Čerin", 76, "CM"), ("A. Bajrić", 74, "CB"),
            ("I. Bijol", 75, "CB"), ("M. Karničnik", 74, "RB"), ("A. Janza", 73, "LB"),
            ("T. Elšnik", 73, "CM"), ("A. Stojanović", 73, "RW"), ("Ž. Senica", 72, "GK"),
            ("L. Šporar", 74, "ST"), ("S. Verbič", 74, "CM"),
            # subs (inc. Šeško the key player)
            ("B. Šeško", 82, "ST"), ("A. Vipotnik", 73, "ST"), ("J. Domen", 72, "CM"),
        ],
    },
    "New Zealand": {
        "ovr": 67, "att": 66, "mid": 66, "def": 67,
        "players": [
            ("C. Wood", 74, "ST"), ("B. Rufer", 72, "LW"), ("C. Rojas", 70, "CM"),
            ("M. McGlinchey", 68, "CAM"), ("T. James", 67, "CM"), ("T. Doyle", 67, "CB"),
            ("M. Jones", 67, "CB"), ("T. Smeltz", 67, "ST"), ("S. Payne", 66, "GK"),
            ("N. Durante", 66, "LB"), ("D. Bell", 66, "RB"),
        ],
    },
    "Honduras": {
        "ovr": 67, "att": 67, "mid": 66, "def": 66,
        "players": [
            ("R. Menjívar", 70, "ST"), ("A. García", 70, "LW"), ("M. Bengtson", 69, "ST"),
            ("O. Boniek García", 69, "CM"), ("E. Izaguirre", 68, "LB"), ("M. Beckeles", 68, "CB"),
            ("J. Velásquez", 67, "CB"), ("E. Álvarez", 67, "RB"), ("D. Turcios", 67, "CM"),
            ("L. Arias", 66, "GK"), ("A. Costly", 67, "RW"),
        ],
    },
    "Panama": {
        "ovr": 69, "att": 68, "mid": 68, "def": 69,
        "players": [
            ("B. Fajardo", 72, "CM"), ("E. Davis", 72, "ST"), ("R. Torres", 72, "CB"),
            ("A. Murillo", 71, "LB"), ("A. Arosemena", 70, "RW"), ("G. Barahona", 70, "CM"),
            ("C. López", 70, "GK"), ("M. Murillo", 71, "CB"), ("F. Abrego", 69, "LW"),
            ("Á. Pinto", 69, "RB"), ("N. Quintero", 69, "CDM"),
            # subs
            ("J. Córdoba", 70, "ST"), ("G. Torres", 69, "LW"), ("A. Galindo", 69, "CM"),
        ],
    },
    "Costa Rica": {
        "ovr": 70, "att": 70, "mid": 69, "def": 70,
        "players": [
            ("B. Ruiz", 77, "ST"), ("C. Bolaños", 74, "CAM"), ("C. Umaña", 72, "CB"),
            ("Ó. Duarte", 72, "CB"), ("D. Myrie", 71, "LB"), ("R. Wass", 71, "RB"),
            ("C. Borges", 71, "CM"), ("D. Colindres", 70, "CM"), ("P. Prendas", 70, "CM"),
            ("L. Moreira", 71, "GK"), ("R. Torres", 70, "LW"),
            # subs
            ("J. Campbell", 73, "LW"), ("A. Contreras", 70, "CM"), ("D. Venegas", 70, "ST"),
        ],
    },
    "Jamaica": {
        "ovr": 67, "att": 68, "mid": 66, "def": 65,
        "players": [
            ("L. Bailey", 80, "LW"), ("D. Junior", 71, "CM"), ("M. Antonio", 74, "ST"),
            ("K. Charles", 69, "RW"), ("D. Morrison", 68, "CB"), ("A. Reid", 68, "CB"),
            ("S. Antonio", 68, "LB"), ("K. Lee", 66, "RB"), ("R. Taylor", 66, "GK"),
            ("C. Williams", 67, "CM"), ("J. Brown", 66, "CDM"),
        ],
    },
    "Qatar": {
        "ovr": 73, "att": 72, "mid": 73, "def": 73,
        "players": [
            ("H. Al-Haydos", 76, "CAM"), ("A. Afif", 78, "LW"), ("K. Boutaib", 73, "ST"),
            ("B. Al-Rawi", 74, "CB"), ("T. Salman", 74, "CB"), ("P. Correia", 73, "RB"),
            ("A. Hassan", 73, "LB"), ("A. Al Haydos", 75, "CM"), ("K. Al-Ghannam", 73, "CDM"),
            ("M. Al-Sheeb", 74, "GK"), ("A. Al-Haidos", 72, "RW"),
        ],
    },
    "Uzbekistan": {
        "ovr": 71, "att": 70, "mid": 71, "def": 70,
        "players": [
            ("E. Shomurodov", 76, "ST"), ("J. Komilov", 72, "CM"), ("O. Akhmedov", 73, "CDM"),
            ("S. Jaloliddinov", 72, "CM"), ("D. Ruziev", 71, "LW"), ("B. Abdusalomov", 70, "CB"),
            ("V. Kobilov", 70, "CB"), ("K. Tillayev", 70, "LB"), ("J. Ortikov", 70, "RB"),
            ("I. Nesterov", 70, "GK"), ("N. Yakhshiboyev", 70, "RW"),
        ],
    },
}


def recompute_top11(players: list) -> float:
    """Average OVR of the first 11 player entries (starters)."""
    first11 = players[:11]
    if not first11:
        return 0.0
    return round(sum(p["ovr"] for p in first11) / len(first11), 1)


def main():
    with open(RATINGS_PATH) as f:
        data = json.load(f)

    teams = data["teams"]
    updated = 0
    skipped = 0

    print(f"\nPatching ratings.json  ({len(teams)} teams in DB, {len(CORRECTIONS)} corrections)\n")

    for team in teams:
        name = team["name"]
        if name not in CORRECTIONS:
            skipped += 1
            continue

        c = CORRECTIONS[name]
        old_ovr = team.get("ovr")

        team["ovr"] = c["ovr"]
        team["att"] = c["att"]
        team["mid"] = c["mid"]
        team["def"] = c["def"]

        # Rebuild players list from correction tuples
        new_players = [
            {"name": p[0], "ovr": p[1], "position": p[2]}
            for p in c["players"]
        ]
        team["players"] = new_players
        team["top11_avg_ovr"] = recompute_top11(new_players)

        new_ovr = team["ovr"]
        new_top11 = team["top11_avg_ovr"]
        delta = new_ovr - old_ovr if old_ovr is not None else 0
        marker = "+" + str(delta) if delta > 0 else str(delta)
        print(f"  {name:<25} OVR {old_ovr} -> {new_ovr}  ({marker})  top11={new_top11}")
        updated += 1

    data["_meta"]["last_updated"] = "2026-06-15"
    data["_meta"]["note"] = (
        "OVR/ATT/MID/DEF from SoFIFA WC 2026 pages (re-verified Jun 15 2026). "
        "top11_avg_ovr recomputed from corrected starter XI. players[] = full squad sorted starters-first."
    )

    with open(RATINGS_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Updated {updated} teams, skipped {skipped} (no correction data)")
    print(f"   Saved → {RATINGS_PATH}")


if __name__ == "__main__":
    main()
