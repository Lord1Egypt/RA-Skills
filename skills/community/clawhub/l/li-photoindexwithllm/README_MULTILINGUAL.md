# 🌍 多语言使用说明 / Multilingual Usage Guide

**作者**: 北京老李（beijingLL）  
**版本**: v1.1.0

---

## 📑 可用语言 / Available Languages

| 语言 | Language | 文件 |
|------|----------|------|
| 🇨🇳 中文（简体） | Chinese (Simplified) | [查看](README_ZH.md) |
| 🇺🇸 English | English | [View](README_EN.md) |
| 🇯🇵 日本語 | Japanese | [表示](README_JA.md) |
| 🇰🇷 한국어 | Korean | [보기](README_KO.md) |
| 🇫🇷 Français | French | [Voir](README_FR.md) |
| 🇩🇪 Deutsch | German | [Ansehen](README_DE.md) |
| 🇪🇸 Español | Spanish | [Ver](README_ES.md) |
| 🇷🇺 Русский | Russian | [Просмотр](README_RU.md) |
| 🇸🇦 العربية | Arabic | [عرض](README_AR.md) |
| 🇧🇷 Português | Portuguese | [Ver](README_PT.md) |

---

## Quick Navigation

Scroll down to find your language:
- [🇨🇳 中文](#-中文简体)
- [🇺🇸 English](#-english)
- [🇯🇵 日本語](#-日本語)
- [🇰🇷 한국어](#-한국어)
- [🇫🇷 Français](#-français)
- [🇩🇪 Deutsch](#-deutsch)
- [🇪🇸 Español](#-español)
- [🇷🇺 Русский](#-русский)
- [🇸🇦 العربية](#-العربية)
- [🇧🇷 Português](#-português)

---

## 🇨🇳 中文（简体）

### 简介

PhotoIndexWithLLM 是一个基于视觉-语言（VL）大模型的智能照片索引和搜索系统。

### 快速开始

```bash
# 安装依赖
pip install requests

# 扫描照片
python skill.py scan --dir D:\Photos

# 搜索照片
python skill.py search "海滩 日落"

# JSON 输出
python skill.py search "海滩" --format json
```

### 支持的平台

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### 隐私保护

- 默认仅使用本地模型
- 照片不会离开您的电脑
- 远程传输需要用户确认

---

## 🇺🇸 English

### Overview

PhotoIndexWithLLM is a smart photo indexing and search system powered by Vision-Language (VL) large models.

### Quick Start

```bash
# Install dependencies
pip install requests

# Scan photos
python skill.py scan --dir /home/user/Photos

# Search photos
python skill.py search "beach sunset"

# JSON output
python skill.py search "beach" --format json
```

### Supported Platforms

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### Privacy Protection

- Local-only by default
- Photos never leave your machine
- Remote transfer requires user consent

---

## 🇯🇵 日本語

### 概要

PhotoIndexWithLLM は、ビジョンランゲージ（VL）大規模モデルを搭載したスマートな写真索引および検索システムです。

### クイックスタート

```bash
# 依存関係をインストール
pip install requests

# 写真をスキャン
python skill.py scan --dir /home/user/Photos

# 写真を検索
python skill.py search "ビーチ 夕日"

# JSON 出力
python skill.py search "ビーチ" --format json
```

### サポートされているプラットフォーム

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### プライバシー保護

- デフォルトでローカルのみ
- 写真はマシンから出ません
- リモート転送にはユーザーの同意が必要

---

## 🇰🇷 한국어

### 개요

PhotoIndexWithLLM 은 비전-언어(VL) 대형 모델 기반의 스마트 사진 인덱싱 및 검색 시스템입니다.

### 빠른 시작

```bash
# 종속성 설치
pip install requests

# 사진 스캔
python skill.py scan --dir /home/user/Photos

# 사진 검색
python skill.py search "바다 석양"

# JSON 출력
python skill.py search "바다" --format json
```

### 지원 플랫폼

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### 개인정보 보호

- 기본적으로 로컬 전용
- 사진이 기기를 벗어나지 않음
- 원격 전송에는 사용자 동의 필요

---

## 🇫🇷 Français

### Aperçu

PhotoIndexWithLLM est un système intelligent d'indexation et de recherche de photos alimenté par des grands modèles Vision-Language (VL).

### Démarrage Rapide

```bash
# Installer les dépendances
pip install requests

# Analyser les photos
python skill.py scan --dir /home/user/Photos

# Rechercher des photos
python skill.py search "plage coucher de soleil"

# Sortie JSON
python skill.py search "plage" --format json
```

### Plateformes Supportées

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### Protection de la Vie Privée

- Local par défaut
- Les photos ne quittent jamais votre machine
- Le transfert à distance nécessite le consentement

---

## 🇩🇪 Deutsch

### Übersicht

PhotoIndexWithLLM ist ein intelligentes Foto-Indizierungs- und Suchsystem, das von Vision-Language (VL) Großmodellen angetrieben wird.

### Schnellstart

```bash
# Abhängigkeiten installieren
pip install requests

# Fotos scannen
python skill.py scan --dir /home/user/Photos

# Fotos suchen
python skill.py search " Strand Sonnenuntergang"

# JSON-Ausgabe
python skill.py search " Strand" --format json
```

### Unterstützte Plattformen

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### Datenschutz

- Standardmäßig nur lokal
- Fotos verlassen niemals Ihr Gerät
- Remote-Übertragung erfordert Benutzerzustimmung

---

## 🇪🇸 Español

### Descripción General

PhotoIndexWithLLM es un sistema inteligente de indexación y búsqueda de fotos impulsado por grandes modelos de Visión-Lenguaje (VL).

### Inicio Rápido

```bash
# Instalar dependencias
pip install requests

# Escanear fotos
python skill.py scan --dir /home/user/Photos

# Buscar fotos
python skill.py search "playa atardecer"

# Salida JSON
python skill.py search "playa" --format json
```

### Plataformas Soportadas

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### Protección de Privacidad

- Solo local por defecto
- Las fotos nunca salen de su máquina
- La transferencia remota requiere consentimiento

---

## 🇷🇺 Русский

### Обзор

PhotoIndexWithLLM — это интеллектуальная система индексации и поиска фотографий на основе больших моделей Vision-Language (VL).

### Быстрый старт

```bash
# Установка зависимостей
pip install requests

# Сканирование фотографий
python skill.py scan --dir /home/user/Photos

# Поиск фотографий
python skill.py search "пляж закат"

# Вывод JSON
python skill.py search "пляж" --format json
```

### Поддерживаемые платформы

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### Защита конфиденциальности

- Только локальный режим по умолчанию
- Фотографии никогда не покидают ваш компьютер
- Удаленная передача требует согласия

---

## 🇸🇦 العربية

### نظرة عامة

PhotoIndexWithLLM هو نظام ذكي لفهرسة الصور والبحث فيها يعتمد على نماذج الرؤية واللغة الكبيرة (VL).

### البدء السريع

```bash
# تثبيت التبعيات
pip install requests

# مسح الصور ضوئياً
python skill.py scan --dir /home/user/Photos

# البحث عن الصور
python skill.py search "شاطئ غروب"

# إخراج JSON
python skill.py search "شاطئ" --format json
```

### المنصات المدعومة

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### حماية الخصوصية

- محلي فقط افتراضياً
- الصور لا تغادر جهازك أبداً
- النقل عن بُعد يتطلب موافقة المستخدم

---

## 🇧🇷 Português

### Visão Geral

PhotoIndexWithLLM é um sistema inteligente de indexação e busca de fotos alimentado por grandes modelos de Visão-Linguagem (VL).

### Início Rápido

```bash
# Instalar dependências
pip install requests

# Escanear fotos
python skill.py scan --dir /home/user/Photos

# Buscar fotos
python skill.py search "praia pôr do sol"

# Saída JSON
python skill.py search "praia" --format json
```

### Plataformas Suportadas

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

### Proteção de Privacidade

- Apenas local por padrão
- As fotos nunca saem da sua máquina
- Transferência remota requer consentimento

---

## 📞 联系方式 / Contact

**作者 / Author**: 北京老李（beijingLL）  
**ClawHub ID**: 43622283  
**项目 / Project**: PhotoIndexWithLLM

---

**祝使用愉快！** 📸✨
