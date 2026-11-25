"""Этап 0. Сбор новостей за последние 24 часа: Telegram-каналы, Google News, (опц.) newsfeed."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm

from .config import ctx
from .utils import HTTP_HEADERS, clean_text_simple, parse_rss_date

TG_CHANNELS = sorted(set([
    "BIoomberg", "data_secrets", "thefutureofwork", "markettwits",
    "rybar_america", "mayday_7700", "prompt_design", "regroup_consulting",
    "abulaphia", "blockchainRF", "forklogAI", "ifax_go", "fm_invest", "rbc_news", "government_rus",
    "centralbank_russia", "frank_media", "newssmartlab", "selfinvestor", "bankrollo", "kommersant",
    "BloombergTerminals", "spimexofficial", "DeCenter", "thebell_io", "minfin", "Bell_tech",
    "zeroton", "xor_journal", "ai_machinelearning_big_data", "parasiticresistance",
    "disruptors_official", "truecon", "proeconomics", "Metals_Mining", "xtxixty", "monocle_media",
    "spydell_finance", "russianmacro", "github", "headlines_MACRO", "infranews",
    "airi_research_institute", "rndml_team", "aioftheday", "curioai", "denissexy",
    "Theedinorogblog", "thegrindingmachine", "tamingofai",
]))

GOOGLE_QUERIES = {
    "US": [
        # Frontier AI и DS
        "OpenAI Anthropic new model release announcement", "AI startup funding round Series raised",
        "Nvidia AMD AI chip news", "Epoch AI report chip deployment trends",
        "White House AI executive order framework", "EU AI Act Commission obligations enforcement",
        "Google DeepMind Gemini release update", "AWS Azure Google Cloud AI capex earnings",
        "AI copyright lawsuit ruling music publishers", "AI company acquisition announced",
        "Mistral Meta xAI announcement", "Crunchbase biggest AI funding rounds this week",
        "Safe Superintelligence funding valuation news", "the-decoder AI news",
        "enterprise AI agents launch product", "open letter AI policy open weights American leadership",
        "Palantir earnings AI results", "AI agent incident safety investigation report",
        "Reddit Perplexity AI lawsuit ruling", "AI infrastructure data center deal gigawatt",
        "state AI law regulation United States", "AI chip export controls Commerce Department China",
        "Samsung SK Hynix HBM earnings AI chip",
        # Робототехника
        "humanoid robot announcement launch", "The Robot Report news", "Figure AI announcement",
        "Unitree news IPO", "FCC import restrictions humanoid robots ruling", "Waymo expansion news",
        "Physical Intelligence Skild AI foundation model robot",
        "Google DeepMind Gemini Robotics announcement", "robotaxi Zoox Nuro news",
        "Agility Robotics Apptronik 1X Figure news", "Amazon robotics warehouse deployment",
        "BYD humanoid robot unveiled", "arXiv robotics VLA vision-language-action paper",
        "Anduril Skydio drone contract announcement", "Boston Dynamics Atlas news",
        "KUKA Fanuc Yaskawa ABB robotics earnings orders", "DoorDash drone delivery announcement",
        "China humanoid robot Galbot UBTech Fourier AgiBot news",
        "Nuro Wayve Pony.ai WeRide announcement funding", "embodied AI startup funding round China",
        "Xpeng IRON humanoid Xiaomi Ant robot announcement", "Hyundai humanoid robots factory deploy",
        "Aurora Innovation Kodiak autonomous trucking results",
        "China robot policy embodied intelligence plan", "medical agricultural robot announcement",
        # Финтех
        "fintech news payments", "Stripe announcement", "stablecoin regulation announcement",
        "Circle USDC news", "Coinbase Block earnings results", "SEC crypto rule proposal",
        "FCA consultation payments", "fintech acquisition announced payments company",
        "Nubank Revolut Klarna Wise news", "RBI CKYC circular rollout",
        "Tether attestation reserves report", "digital euro ECB European Parliament regulation",
        "Ripple SWIFT Visa Mastercard stablecoin announcement",
        "tokenization tokenized funds announcement BlackRock JPMorgan",
        "crypto stablecoin regulation Treasury GENIUS Act", "PhonePe IPO India fintech",
        "ledger insights tokenization CBDC news", "CLARITY Act market structure crypto bill vote",
        "MAS Monetary Authority Singapore stablecoin digital asset",
        "Flutterwave acquisition bank announcement", "Kraken Payward acquisition wallet infrastructure",
        "HSBC Blackstone loan portfolio sale announcement",
        "OpenAI", "Anthropic", "LLM", "AI", "Deepseek", "Nvidia",
    ],
    "CH": [
        # Китай и Азия
        "DeepSeek new model release", "Alibaba Qwen release", "Huawei Ascend chip announcement",
        "Moonshot Kimi Zhipu MiniMax announcement", "Unitree UBTech humanoid robot news",
        "HKMA stablecoin licence Hong Kong", "China chip export control response Nvidia SMIC Cambricon",
        "Zhipu MiniMax Hong Kong IPO listing HKEX", "Ant Group PBoC digital yuan announcement",
        "China AI regulation CAC MIIT news", "Japan Korea AI robotics news SoftBank Samsung Naver",
        "ByteDance Doubao Seed model release", "AgiBot Galbot Fourier robot funding round",
        "Tencent Hunyuan Baidu Ernie release", "Cambricon SMIC earnings results",
        "China humanoid robot policy government plan", "SCMP China tech news",
        "Caixin Global technology finance news", "India AI policy fintech UPI news",
        "Hong Kong stablecoin issuer licence granted", "Xpeng IRON humanoid mass production",
        "Nvidia H200 China customs approval ban", "Korea Samsung SK Hynix AI chip news",
        "Japan Sakana AI SoftBank announcement", "Moore Threads Biren Cambricon AI chip China domestic",
        "MiniMax open weights model release", "Seedance ByteDance video model release",
        "DeepSeek 新模型 发布", "阿里巴巴 通义千问 Qwen 发布", "华为 昇腾 芯片 发布",
        "月之暗面 Kimi 智谱 MiniMax 发布", "宇树 优必选 人形机器人 新闻", "宇树科技 科创板 IPO 招股",
        "香港金管局 稳定币 牌照", "中国 芯片 出口管制 英伟达 中芯国际 寒武纪", "智谱 MiniMax 香港上市 招股",
        "蚂蚁集团 央行 数字人民币 公告", "中国 人工智能 监管 网信办 工信部", "字节跳动 豆包 Seed 模型 发布",
        "智元 银河通用 傅利叶 机器人 融资", "腾讯 混元 百度 文心一言 发布", "寒武纪 中芯国际 财报 业绩",
        "中国 人形机器人 产业政策 规划", "南华早报 中国科技新闻", "财新 科技 财经 新闻",
        "印度 人工智能 政策 UPI 新闻", "香港 稳定币 发牌 新一批", "小鹏 IRON 人形机器人 量产",
        "英伟达 H200 中国 海关 审批 禁令", "三星 SK海力士 AI芯片 新闻", "日本 Sakana AI 软银 公告",
        "摩尔线程 壁仞 寒武纪 国产AI芯片", "MiniMax 开源模型 发布", "字节跳动 即梦 Seedance 视频模型 发布",
        "36氪 机器人 人工智能 早报", "具身智能 国家人工智能应用中心 揭牌", "中国 金融监管 稳定币 人民币 新规",
    ],
    "RU": [
        # Россия и СНГ
        "Сбер GigaChat релиз", "ЦБ РФ цифровой рубль новости", "Банк России пресс-релиз",
        "Яндекс новости нейросеть Алиса", "Яндекс финансовые результаты отчетность",
        "Сбербанк результаты РПБУ прибыль", "робототехника Россия роботизация промышленные роботы",
        "искусственный интеллект Россия запуск", "Kaspi Freedom Holding Казахстан финтех результаты",
        "вступают в силу законы банки переводы",
        "законопроект регулирование искусственного интеллекта Госдума",
        "закон о регулировании искусственного интеллекта Россия",
        "Hugging Face Russian open model release GigaChat T-Bank",
        "беспилотные автомобили Яндекс робот доставка закон", "универсальный QR код НСПК банки",
        "федеральный проект развитие промышленной робототехники финансирование",
        "VK результаты отчет МСФО", "Ozon Финтех результаты",
        "Московская биржа объемы торгов пресс-релиз", "Сбер новости искусственный интеллект",
        "гуманоидный робот Россия презентация", "Frank Media банки новости",
        "Казахстан Нацбанк цифровой тенге новости", "MWS AI МТС модель Cotype",
        "Т-Банк ИИ агент запуск", "Росфинмониторинг криптовалюта отчетность закон",
        "правительство перечень предустанавливаемого российского ПО распоряжение",
    ],
}

GOOGLE_TOPICS = ["BUSINESS", "TECHNOLOGY", "SCIENCE"]


def _since() -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=1)


# ---------------- Telegram ----------------
def collect_telegram() -> int:
    import snscrape.modules.telegram as sntelegram

    since = _since()
    posts = []
    for channel in tqdm(TG_CHANNELS, desc="telegram"):
        try:
            for post in sntelegram.TelegramChannelScraper(channel).get_items():
                date = post.date if post.date.tzinfo else post.date.replace(tzinfo=timezone.utc)
                content = str(post.content or "")
                if date < since:
                    break
                if len(content) <= 50:
                    continue
                posts.append({
                    "type": "telegram",
                    "source": f"@{channel}",
                    "url": post.url,
                    "date": date.strftime("%Y-%m-%d"),
                    "time": date.strftime("%H:%M"),
                    "original": content,
                    "description": clean_text_simple(content),
                })
        except Exception as e:
            logger.warning(f"Telegram @{channel}: {e}")

    df = pd.DataFrame(posts)
    if not df.empty:
        df["id"] = range(1, len(df) + 1)
        df.to_csv(ctx().tg_csv, header=True)
    logger.info(f"Собрано {len(df)} телеграм-постов")
    return len(df)


# ---------------- Google News ----------------
def _rss_items(url: str, params: dict) -> list:
    r = requests.get(url, params=params, headers=HTTP_HEADERS, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "xml").find_all("item")


def _row(item, query: str) -> dict | None:
    dt = parse_rss_date(item.find("pubDate").text) if item.find("pubDate") else None
    if dt is None or dt < _since():
        return None
    title = item.find("title").text
    return {
        "type": "google_news",
        "query": query,
        "url": item.find("link").text,
        "original": title,
        "description": clean_text_simple(title),
        "source": item.find("source").text if item.find("source") else "",
        "date": dt.strftime("%Y-%m-%d %H-%M"),
        "time": dt.strftime("%H-%M"),
    }


def collect_google_news() -> int:
    posts = []
    for geo, queries in GOOGLE_QUERIES.items():
        for q in tqdm(queries, desc=f"google {geo}"):
            try:
                for item in _rss_items("https://news.google.com/rss/search",
                                       {"q": f"{q} when:1d", "gl": geo}):
                    row = _row(item, q)
                    if row:
                        posts.append(row)
            except Exception as e:
                logger.warning(f"Google News '{q}': {e}")

    for topic in GOOGLE_TOPICS:
        try:
            for item in _rss_items(
                    f"https://news.google.com/news/rss/headlines/section/topic/{topic}", {"gl": "US"}):
                row = _row(item, f"TOPIC: {topic}")
                if row:
                    posts.append(row)
        except Exception as e:
            logger.warning(f"Google News topic {topic}: {e}")

    df = pd.DataFrame(posts)
    if not df.empty:
        df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)
        df["id"] = range(1, len(df) + 1)
        df.to_csv(ctx().google_csv, header=True)
    logger.info(f"Собрано {len(df)} новостей Google News")
    return len(df)


# ---------------- newsfeed (опционально) ----------------
def collect_newsfeed() -> int:
    """Доп. источник `newsfeed` (пакет из legacy-проекта). Если пакета нет — пропускаем."""
    try:
        import newsfeed.run as claude_parsing  # type: ignore
    except ImportError:
        logger.info("Пакет newsfeed не найден — источник claude_news пропущен")
        return 0

    c = ctx()
    items = claude_parsing.collect(hours=26, workers=12)
    xlsx_path = claude_parsing.save(items, str(c.claude_dir))
    df = pd.read_excel(xlsx_path)
    df["description"] = df["title"]
    df["type"] = "google_news"
    df = df.rename(columns={"published": "date"})
    df["id"] = range(1, len(df) + 1)
    df = df[["type", "source", "description", "date", "url", "id"]]
    out = c.claude_dir / f"{c.ts}.xlsx"
    df.to_excel(out, index=False)
    c.claude_xlsx = out
    logger.info(f"Собрано {len(df)} новостей newsfeed")
    return len(df)
