#!/usr/bin/env python3
"""
Pokeinfo Unit Tests - Multi-language support
Run: python3 -m pytest tests/test_pokeinfo.py -v
     or: python3 tests/test_pokeinfo.py
"""

import unittest
import sys
import os
import json
import tempfile
import shutil

# Add parent directory to path to import pokeinfo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import pokeinfo


class TestLanguageSupport(unittest.TestCase):
    """Test multi-language functionality."""
    
    def setUp(self):
        """Set up test environment with temp config."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_config_file = pokeinfo.CONFIG_FILE
        pokeinfo.CONFIG_FILE = os.path.join(self.temp_dir, 'config.json')
    
    def tearDown(self):
        """Clean up temp files."""
        shutil.rmtree(self.temp_dir)
        pokeinfo.CONFIG_FILE = self.original_config_file
    
    def test_all_supported_languages(self):
        """Test that all 9 languages are supported."""
        expected_langs = ['en', 'zh-hant', 'zh-hans', 'ja', 'ko', 'fr', 'de', 'es', 'it']
        for lang in expected_langs:
            self.assertIn(lang, pokeinfo.TRANSLATIONS)
            self.assertIn(lang, pokeinfo.LANG_DISPLAY)
    
    def test_language_setting(self):
        """Test setting and getting language."""
        # Default should be English
        self.assertEqual(pokeinfo.get_lang(), 'en')
        
        # Test setting each language
        for lang in ['zh-hant', 'zh-hans', 'ja', 'ko']:
            config = pokeinfo.load_config()
            config['language'] = lang
            pokeinfo.save_config(config)
            self.assertEqual(pokeinfo.get_lang(), lang)
    
    def test_translation_keys_complete(self):
        """Test that all languages have complete translation keys."""
        required_keys = [
            'height', 'weight', 'base_exp', 'types', 'abilities', 'hidden',
            'stats', 'hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed',
            'sprite', 'cry', 'moves', 'language_set', 'available_langs',
            'unknown_lang', 'not_found'
        ]
        
        for lang, translations in pokeinfo.TRANSLATIONS.items():
            for key in required_keys:
                self.assertIn(key, translations, f"Missing key '{key}' in language '{lang}'")
    
    def test_english_translation(self):
        """Test English translations."""
        self.assertEqual(pokeinfo.t('height', 'en'), 'Height')
        self.assertEqual(pokeinfo.t('weight', 'en'), 'Weight')
        self.assertEqual(pokeinfo.t('types', 'en'), 'Type(s)')
        self.assertEqual(pokeinfo.t('abilities', 'en'), 'Abilities')
        self.assertEqual(pokeinfo.t('hidden', 'en'), 'Hidden')
    
    def test_traditional_chinese_translation(self):
        """Test Traditional Chinese translations."""
        self.assertEqual(pokeinfo.t('height', 'zh-hant'), '身高')
        self.assertEqual(pokeinfo.t('weight', 'zh-hant'), '體重')
        self.assertEqual(pokeinfo.t('types', 'zh-hant'), '屬性')
        self.assertEqual(pokeinfo.t('abilities', 'zh-hant'), '特性')
        self.assertEqual(pokeinfo.t('hidden', 'zh-hant'), '隱藏特性')
        self.assertEqual(pokeinfo.t('stats', 'zh-hant'), '六項數值')
        self.assertEqual(pokeinfo.t('attack', 'zh-hant'), '攻擊')
        self.assertEqual(pokeinfo.t('defense', 'zh-hant'), '防禦')
    
    def test_simplified_chinese_translation(self):
        """Test Simplified Chinese translations."""
        self.assertEqual(pokeinfo.t('height', 'zh-hans'), '身高')
        self.assertEqual(pokeinfo.t('weight', 'zh-hans'), '体重')
        self.assertEqual(pokeinfo.t('types', 'zh-hans'), '属性')
        self.assertEqual(pokeinfo.t('hidden', 'zh-hans'), '隐藏特性')
    
    def test_japanese_translation(self):
        """Test Japanese translations."""
        self.assertEqual(pokeinfo.t('height', 'ja'), '身長')
        self.assertEqual(pokeinfo.t('weight', 'ja'), '体重')
        self.assertEqual(pokeinfo.t('types', 'ja'), 'タイプ')
        self.assertEqual(pokeinfo.t('stats', 'ja'), '種族値')
    
    def test_korean_translation(self):
        """Test Korean translations."""
        self.assertEqual(pokeinfo.t('height', 'ko'), '키')
        self.assertEqual(pokeinfo.t('weight', 'ko'), '몸무게')
        self.assertEqual(pokeinfo.t('types', 'ko'), '타입')
        self.assertEqual(pokeinfo.t('stats', 'ko'), '종족값')
    
    def test_french_translation(self):
        """Test French translations."""
        self.assertEqual(pokeinfo.t('height', 'fr'), 'Taille')
        self.assertEqual(pokeinfo.t('weight', 'fr'), 'Poids')
        self.assertEqual(pokeinfo.t('types', 'fr'), 'Type(s)')
        self.assertEqual(pokeinfo.t('stats', 'fr'), 'Stats')
    
    def test_german_translation(self):
        """Test German translations."""
        self.assertEqual(pokeinfo.t('height', 'de'), 'Größe')
        self.assertEqual(pokeinfo.t('weight', 'de'), 'Gewicht')
        self.assertEqual(pokeinfo.t('types', 'de'), 'Typ(en)')
        self.assertEqual(pokeinfo.t('stats', 'de'), 'Werte')
    
    def test_spanish_translation(self):
        """Test Spanish translations."""
        self.assertEqual(pokeinfo.t('height', 'es'), 'Altura')
        self.assertEqual(pokeinfo.t('weight', 'es'), 'Peso')
        self.assertEqual(pokeinfo.t('types', 'es'), 'Tipo(s)')
        self.assertEqual(pokeinfo.t('stats', 'es'), 'Estadísticas')
    
    def test_italian_translation(self):
        """Test Italian translations."""
        self.assertEqual(pokeinfo.t('height', 'it'), 'Altezza')
        self.assertEqual(pokeinfo.t('weight', 'it'), 'Peso')
        self.assertEqual(pokeinfo.t('types', 'it'), 'Tipo(i)')
        self.assertEqual(pokeinfo.t('stats', 'it'), 'Statistiche')


class TestStatNames(unittest.TestCase):
    """Test stat name localization."""
    
    def test_stat_names_english(self):
        """Test English stat names."""
        self.assertEqual(pokeinfo.get_stat_name('hp', 'en'), 'HP')
        self.assertEqual(pokeinfo.get_stat_name('attack', 'en'), 'Attack')
        self.assertEqual(pokeinfo.get_stat_name('defense', 'en'), 'Defense')
        self.assertEqual(pokeinfo.get_stat_name('special-attack', 'en'), 'Sp. Attack')
        self.assertEqual(pokeinfo.get_stat_name('special-defense', 'en'), 'Sp. Defense')
        self.assertEqual(pokeinfo.get_stat_name('speed', 'en'), 'Speed')
    
    def test_stat_names_chinese(self):
        """Test Chinese stat names."""
        self.assertEqual(pokeinfo.get_stat_name('attack', 'zh-hant'), '攻擊')
        self.assertEqual(pokeinfo.get_stat_name('defense', 'zh-hant'), '防禦')
        self.assertEqual(pokeinfo.get_stat_name('special-attack', 'zh-hant'), '特攻')
        self.assertEqual(pokeinfo.get_stat_name('speed', 'zh-hant'), '速度')
        
        self.assertEqual(pokeinfo.get_stat_name('attack', 'zh-hans'), '攻击')
        self.assertEqual(pokeinfo.get_stat_name('defense', 'zh-hans'), '防御')
    
    def test_stat_names_japanese(self):
        """Test Japanese stat names."""
        self.assertEqual(pokeinfo.get_stat_name('attack', 'ja'), 'こうげき')
        self.assertEqual(pokeinfo.get_stat_name('defense', 'ja'), 'ぼうぎょ')
        self.assertEqual(pokeinfo.get_stat_name('speed', 'ja'), 'すばやさ')


class TestLanguageList(unittest.TestCase):
    """Test language listing functionality."""
    
    def test_language_display_names(self):
        """Test that all languages have display names."""
        expected = {
            'en': 'English',
            'zh-hant': '繁體中文',
            'zh-hans': '简体中文',
            'ja': '日本語',
            'ko': '한국어',
            'fr': 'Français',
            'de': 'Deutsch',
            'es': 'Español',
            'it': 'Italiano',
        }
        self.assertEqual(pokeinfo.LANG_DISPLAY, expected)


class TestConfigManagement(unittest.TestCase):
    """Test configuration file management."""
    
    def setUp(self):
        """Set up temp config."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_config_file = pokeinfo.CONFIG_FILE
        pokeinfo.CONFIG_FILE = os.path.join(self.temp_dir, 'config.json')
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir)
        pokeinfo.CONFIG_FILE = self.original_config_file
    
    def test_load_default_config(self):
        """Test loading config when file doesn't exist."""
        config = pokeinfo.load_config()
        self.assertEqual(config['language'], 'en')
    
    def test_save_and_load_config(self):
        """Test saving and loading config."""
        config = {'language': 'zh-hant'}
        pokeinfo.save_config(config)
        
        loaded = pokeinfo.load_config()
        self.assertEqual(loaded['language'], 'zh-hant')
    
    def test_invalid_language_fallback(self):
        """Test fallback to English for invalid language."""
        config = {'language': 'invalid-lang'}
        pokeinfo.save_config(config)
        
        # get_lang should fallback to 'en' for invalid languages
        lang = pokeinfo.get_lang()
        self.assertEqual(lang, 'en')


class TestFormatOutput(unittest.TestCase):
    """Test output formatting."""
    
    def setUp(self):
        """Set up temp config."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_config_file = pokeinfo.CONFIG_FILE
        pokeinfo.CONFIG_FILE = os.path.join(self.temp_dir, 'config.json')
    
    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir)
        pokeinfo.CONFIG_FILE = self.original_config_file
    
    def test_format_with_localized_name(self):
        """Test formatting includes localized name."""
        # Mock data similar to Pikachu
        data = {
            'id': 25,
            'name': 'pikachu',
            'height': 4,
            'weight': 60,
            'base_experience': 112,
            'types': [
                {'type': {'name': 'electric', 'url': 'https://pokeapi.co/api/v2/type/13/'}}
            ],
            'abilities': [
                {'ability': {'name': 'static', 'url': 'https://pokeapi.co/api/v2/ability/9/'}, 'is_hidden': False},
                {'ability': {'name': 'lightning-rod', 'url': 'https://pokeapi.co/api/v2/ability/31/'}, 'is_hidden': True}
            ],
            'stats': [
                {'stat': {'name': 'hp'}, 'base_stat': 35},
                {'stat': {'name': 'attack'}, 'base_stat': 55},
            ],
            'sprites': {
                'other': {'official-artwork': {'front_default': 'https://example.com/pikachu.png'}},
                'front_default': 'https://example.com/pikachu-default.png'
            },
            'cries': {'latest': 'https://example.com/pikachu.ogg'},
            'moves': []
        }
        
        # Test English formatting
        output = pokeinfo.format_pokemon(data, 'en')
        self.assertIn('Pikachu', output)
        self.assertIn('Height:', output)
        self.assertIn('Type(s):', output)
        
        # Test Chinese formatting
        output_zh = pokeinfo.format_pokemon(data, 'zh-hant')
        self.assertIn('身高:', output_zh)
        self.assertIn('屬性:', output_zh)
        self.assertIn('特性:', output_zh)
        self.assertIn('六項數值:', output_zh)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLanguageSupport))
    suite.addTests(loader.loadTestsFromTestCase(TestStatNames))
    suite.addTests(loader.loadTestsFromTestCase(TestLanguageList))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatOutput))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
