/*
Design reminder (commitment): Swiss‑brutalist editorial
- Big serif headlines, mono metadata, lots of whitespace
- Asymmetric layout: sticky left rail + long-scroll narrative
- Crisp rules, occasional red accent, no gradients
*/

import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "wouter";
import { AnimatePresence, motion } from "framer-motion";
import { Play, Pause, ArrowUpRight, Volume2, ChevronDown } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Separator } from "@/components/ui/separator";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { cn } from "@/lib/utils";

import data from "@/assets/highlights.json";
import coverUrl from "@/assets/cover.jpg";

type Lang = "en" | "ja" | "zh";

const UI: Record<
  Lang,
  {
    eyebrow: string;
    subhead: string;
    toc: string;
    show: string;
    host: string;
    guest: string;
    length: string;
    openInApple: string;
    episode: string;
    playClip: string;
    pause: string;
    backToTop: string;
    takeaway: string;
    timestamp: string;
    listenFull: string;
    closingEyebrow: string;
    closingTitle: string;
    curated: string;
    originalEn: string;
    showOriginal: string;
    hideOriginal: string;
  }
> = {
  en: {
    eyebrow: "Inside the episode",
    subhead:
      "A curated set of moments worth rereading—ideas, warnings, and practical moves from a 2‑hour conversation.",
    toc: "Table of contents",
    show: "SHOW",
    host: "{UI[lang].host}",
    guest: "{UI[lang].guest}",
    length: "{UI[lang].length}",
    openInApple: "{UI[lang].openInApple}",
    episode: "EPISODE",
    playClip: "Play clip",
    pause: "Pause",
    backToTop: "Back to top",
    takeaway: "Takeaway",
    timestamp: "Timestamp",
    listenFull: "LISTEN TO FULL EPISODE",
    closingEyebrow: "Closing",
    closingTitle: "A reader's summary",
    curated: "Curated highlights with original audio clips.",
    originalEn: "Original (English)",
    showOriginal: "Show original",
    hideOriginal: "Hide original",
  },
  ja: {
    eyebrow: "エピソードの要点",
    subhead:
      "2時間の対談から、読み返す価値のある瞬間だけを抽出。主張・警告・実践のヒントを、音声クリップ付きで。",
    toc: "目次",
    show: "番組",
    host: "ホスト",
    guest: "ゲスト",
    length: "長さ",
    openInApple: "Apple Podcastsで開く",
    episode: "エピソード",
    playClip: "クリップ再生",
    pause: "一時停止",
    backToTop: "先頭へ",
    takeaway: "要点",
    timestamp: "タイムスタンプ",
    listenFull: "全編を聴く",
    closingEyebrow: "まとめ",
    closingTitle: "読者向け要約",
    curated: "厳選ハイライト（原音クリップ付き）",
    originalEn: "原文（英語）",
    showOriginal: "原文を表示",
    hideOriginal: "原文を隠す",
  },
  zh: {
    eyebrow: "本期精华",
    subhead:
      "从两小时对谈中挑出最值得反复阅读的片段：观点、警告与可执行的动作，并配原声音频。",
    toc: "目录",
    show: "节目",
    host: "主持",
    guest: "嘉宾",
    length: "时长",
    openInApple: "在 Apple Podcasts 打开",
    episode: "单集",
    playClip: "播放片段",
    pause: "暂停",
    backToTop: "回到顶部",
    takeaway: "解读",
    timestamp: "时间戳",
    listenFull: "收听完整单集",
    closingEyebrow: "结语",
    closingTitle: "读者版总结",
    curated: "精选片段（原声可播放）",
    originalEn: "英文原句",
    showOriginal: "展开原句",
    hideOriginal: "收起原句",
  },
};

type Highlight = (typeof data)["highlights"][number];

function formatDuration(sec: number) {
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  return h ? `${h}h ${m}m` : `${m}m`;
}

function formatTimecode(sec: number) {
  const s = Math.max(0, Math.floor(sec));
  const hh = Math.floor(s / 3600);
  const mm = Math.floor((s % 3600) / 60);
  const ss = s % 60;
  if (hh) return `${hh}:${String(mm).padStart(2, "0")}:${String(ss).padStart(2, "0")}`;
  return `${mm}:${String(ss).padStart(2, "0")}`;
}

function t(h: Highlight, lang: Lang, key: "quote" | "takeaway" | "context") {
  const k = `${key}_${lang}` as const;
  return (h as any)[k] as string;
}

function titleFor(h: Highlight, lang: Lang) {
  if (lang === "en") return (h as any).title_en ?? h.title;
  return (h as any)[`title_${lang}`] ?? h.title;
}

function displayFont(lang: Lang) {
  if (lang === "ja") return "var(--font-display-ja)";
  if (lang === "zh") return "var(--font-display-zh)";
  return "var(--font-display)";
}

function bodyFont(lang: Lang) {
  if (lang === "ja") return "var(--font-body-ja)";
  if (lang === "zh") return "var(--font-body-zh)";
  return "var(--font-body)";
}

function clamp(n: number, a: number, b: number) {
  return Math.min(b, Math.max(a, n));
}

function useScrollProgress() {
  const [progress, setProgress] = useState(0);
  useEffect(() => {
    const onScroll = () => {
      const el = document.documentElement;
      const max = Math.max(1, el.scrollHeight - el.clientHeight);
      setProgress(clamp(el.scrollTop / max, 0, 1));
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return progress;
}

export default function Home({ targetSection }: { targetSection?: string }) {
  const [lang, setLang] = useState<Lang>("en");

  // Make language truly global (CSS + typography)
  useEffect(() => {
    document.documentElement.setAttribute("data-lang", lang);
    return () => {
      // keep last set
    };
  }, [lang]);
  const [activeId, setActiveId] = useState<string>(data.highlights[0]?.id ?? "");
  const [nowPlaying, setNowPlaying] = useState<string | null>(null);
  const [isPaused, setIsPaused] = useState(false);
  const [openOriginal, setOpenOriginal] = useState<Record<string, boolean>>({});

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const progress = useScrollProgress();

  // --- Audio URL map
  const audioUrlMap = useMemo(() => {
    const modules = import.meta.glob("../assets/audio/*.mp3", {
      eager: true,
      query: "?url",
      import: "default",
    }) as Record<string, string>;

    const map: Record<string, string> = {};
    for (const [path, url] of Object.entries(modules)) {
      const file = path.split("/").pop() || "";
      const id = file.replace(".mp3", "");
      map[id] = url;
    }
    return map;
  }, []);

  // Scroll to section when URL changes
  useEffect(() => {
    if (targetSection) {
      document.getElementById(targetSection)?.scrollIntoView({ behavior: "smooth" });
    }
  }, [targetSection]);

  // Track active section via IntersectionObserver
  useEffect(() => {
    const ids = data.highlights.map((h) => h.id);
    const els = ids
      .map((id) => document.getElementById(id))
      .filter(Boolean) as HTMLElement[];

    if (!els.length) return;

    const obs = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => (a.boundingClientRect.top ?? 0) - (b.boundingClientRect.top ?? 0));
        if (visible[0]?.target?.id) setActiveId(visible[0].target.id);
      },
      { root: null, threshold: 0.35 }
    );

    els.forEach((el) => obs.observe(el));
    return () => obs.disconnect();
  }, []);

  // Keep audio state consistent
  useEffect(() => {
    if (!audioRef.current) return;
    const a = audioRef.current;

    const onEnded = () => {
      setNowPlaying(null);
      setIsPaused(false);
    };

    const onPause = () => {
      // pause fires also when source changes
      if (nowPlaying) setIsPaused(true);
    };

    const onPlay = () => {
      if (nowPlaying) setIsPaused(false);
    };

    a.addEventListener("ended", onEnded);
    a.addEventListener("pause", onPause);
    a.addEventListener("play", onPlay);
    return () => {
      a.removeEventListener("ended", onEnded);
      a.removeEventListener("pause", onPause);
      a.removeEventListener("play", onPlay);
    };
  }, [nowPlaying]);

  const play = async (id: string) => {
    const url = audioUrlMap[id];
    if (!url) return;

    if (!audioRef.current) audioRef.current = new Audio();
    const a = audioRef.current;

    if (nowPlaying === id) {
      if (a.paused) {
        await a.play();
      } else {
        a.pause();
      }
      return;
    }

    setNowPlaying(id);
    setIsPaused(false);
    a.src = url;
    a.currentTime = 0;
    a.volume = 0.95;
    await a.play();
  };

  const stop = () => {
    const a = audioRef.current;
    if (!a) return;
    a.pause();
    a.currentTime = 0;
    setNowPlaying(null);
    setIsPaused(false);
  };

  return (
    <div className="min-h-screen">
      {/* Grain overlay */}
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 z-0 opacity-[0.07] mix-blend-multiply"
        style={{
          backgroundImage:
            "url(data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='.35'/%3E%3C/svg%3E)",
        }}
      />

      {/* Progress bar */}
      <div className="fixed left-0 top-0 z-50 h-[3px] w-full bg-transparent">
        <div
          className="h-full bg-primary"
          style={{ width: `${Math.round(progress * 100)}%` }}
        />
      </div>

      <div className="relative z-10 mx-auto max-w-[1200px] px-5 py-10 md:px-10 md:py-14">
        <div className="grid grid-cols-1 gap-10 md:grid-cols-[300px_1fr] md:gap-14">
          {/* Left rail */}
          <aside className="md:sticky md:top-10 md:self-start">
            <div className="space-y-6">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div
                    className="text-xs uppercase tracking-[0.22em] text-muted-foreground"
                    style={{ fontFamily: "var(--font-mono)" }}
                  >
                    {UI[lang].eyebrow}
                  </div>
                  <div
                    className="mt-2 text-2xl leading-[1.05]"
                    style={{ fontFamily: displayFont(lang) }}
                  >
                    {data.hero.title_lines[0]}
                  </div>
                  <div
                    className="mt-1 text-2xl leading-[1.05]"
                    style={{ fontFamily: displayFont(lang) }}
                  >
                    {data.hero.title_lines[1]}
                  </div>
                </div>

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button
                      variant="outline"
                      className="h-9 gap-2 rounded-full border-border bg-background/60 px-3 backdrop-blur"
                    >
                      <span
                        className="text-xs font-medium"
                        style={{ fontFamily: "var(--font-mono)" }}
                      >
                        {lang.toUpperCase()}
                      </span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" className="min-w-36">
                    <DropdownMenuItem onClick={() => setLang("en")}>English</DropdownMenuItem>
                    <DropdownMenuItem onClick={() => setLang("ja")}>日本語</DropdownMenuItem>
                    <DropdownMenuItem onClick={() => setLang("zh")}>中文</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>

              <p className="text-sm leading-relaxed text-muted-foreground">{UI[lang].subhead}</p>

              <Card className="rounded-2xl border-border bg-card/70 p-4 backdrop-blur">
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span style={{ fontFamily: "var(--font-mono)" }}>{UI[lang].show}</span>
                  <Separator orientation="vertical" className="h-4" />
                  <span className="text-foreground">{data.podcast.show}</span>
                </div>
                <div className="mt-2 grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
                  <div className="text-muted-foreground" style={{ fontFamily: "var(--font-mono)" }}>
                    {UI[lang].host}
                  </div>
                  <div className="text-foreground">{data.podcast.host}</div>
                  <div className="text-muted-foreground" style={{ fontFamily: "var(--font-mono)" }}>
                    {UI[lang].guest}
                  </div>
                  <div className="text-foreground">{data.podcast.guest}</div>
                  <div className="text-muted-foreground" style={{ fontFamily: "var(--font-mono)" }}>
                    {UI[lang].length}
                  </div>
                  <div className="text-foreground">{formatDuration(data.podcast.duration_sec)}</div>
                </div>
                <Separator className="my-3" />
                <a
                  className="group inline-flex items-center gap-2 text-xs text-foreground"
                  href={data.podcast.source_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  <span style={{ fontFamily: "var(--font-mono)" }}>{UI[lang].openInApple}</span>
                  <ArrowUpRight className="h-4 w-4 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
                </a>
              </Card>

              <div className="rounded-2xl border border-border bg-background/50 p-4 backdrop-blur">
                <div
                  className="text-xs uppercase tracking-[0.22em] text-muted-foreground"
                  style={{ fontFamily: "var(--font-mono)" }}
                >
                  {UI[lang].toc}
                </div>

                <div className="mt-3 space-y-1">
                  {data.highlights.map((h, idx) => {
                    const isActive = h.id === activeId;
                    return (
                      <Link
                        key={h.id}
                        href={`/${h.id}`}
                        className={cn(
                          "group relative flex items-baseline gap-3 rounded-xl px-2 py-2 transition-colors",
                          "outline-none focus-visible:ring-2 focus-visible:ring-ring",
                          isActive
                            ? "bg-secondary text-foreground"
                            : "text-foreground/90 hover:bg-secondary/60"
                        )}
                      >
                        <span
                          aria-hidden
                          className={cn(
                            "absolute left-0 top-1/2 h-[70%] w-[2px] -translate-y-1/2 rounded-full transition-colors",
                            isActive ? "bg-primary" : "bg-transparent group-hover:bg-border"
                          )}
                        />
                        <span
                          className={cn(
                            "text-[11px]",
                            isActive ? "text-primary" : "text-muted-foreground"
                          )}
                          style={{ fontFamily: "var(--font-mono)" }}
                        >
                          {String(idx + 1).padStart(2, "0")}
                        </span>
                        <span className={cn("text-sm", isActive ? "text-foreground" : "text-foreground/90")}>
                          {titleFor(h, lang)}
                        </span>
                      </Link>
                    );
                  })}
                </div>

                <AnimatePresence>
                  {nowPlaying && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 8 }}
                      className="mt-4 flex items-center justify-between rounded-xl bg-primary px-3 py-2 text-primary-foreground"
                    >
                      <div className="flex items-center gap-2">
                        <Volume2 className="h-4 w-4" />
                        <div className="text-xs" style={{ fontFamily: "var(--font-mono)" }}>
                          {lang === "en" ? "PLAYING" : lang === "ja" ? "再生中" : "正在播放"}{" "}
                          {nowPlaying.toUpperCase()}
                        </div>
                      </div>
                      <Button
                        size="sm"
                        variant="secondary"
                        className="h-8 rounded-full"
                        onClick={stop}
                      >
                        {lang === "en" ? "Stop" : lang === "ja" ? "停止" : "停止"}
                      </Button>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </aside>

          {/* Main narrative */}
          <main className="space-y-10">
            {/* Hero (no full-bleed cover image) */}
            <section
              id="top"
              className="relative overflow-hidden rounded-[28px] border border-border bg-background/70 backdrop-blur"
            >
              <div aria-hidden className="absolute inset-0">
                {/* Soft paper gradient + subtle rules */}
                <div className="absolute inset-0 bg-[radial-gradient(1000px_600px_at_20%_10%,oklch(0.99_0.01_85)_0%,transparent_60%),radial-gradient(900px_500px_at_80%_0%,oklch(0.94_0.03_85)_0%,transparent_55%)]" />
                <div className="absolute inset-0 opacity-[0.22] [background-image:linear-gradient(to_bottom,transparent_0,transparent_14px,oklch(0.16_0.02_40/0.12)_14px,oklch(0.16_0.02_40/0.12)_15px)] [background-size:100%_15px]" />
                <div className="absolute inset-0 ring-1 ring-inset ring-border" />
              </div>

              <div className="relative px-6 py-9 md:px-10 md:py-12">
                <div
                  className="inline-flex items-center gap-2 rounded-full bg-background/70 px-3 py-1.5 text-xs text-foreground backdrop-blur"
                  style={{ fontFamily: "var(--font-mono)" }}
                >
                  <span className="text-muted-foreground">{UI[lang].episode}</span>
                  <span className="text-primary">{data.podcast.published}</span>
                  <span className="text-muted-foreground">•</span>
                  <span>{formatDuration(data.podcast.duration_sec)}</span>
                </div>

                <div className="mt-5 grid gap-6 md:grid-cols-[1fr_170px] md:items-start">
                  <div className="min-w-0">
                    <h1
                      className="text-4xl leading-[0.95] tracking-tight md:text-6xl"
                      style={{ fontFamily: displayFont(lang) }}
                    >
                      {data.podcast.title}
                    </h1>

                    <p className="mt-4 max-w-2xl text-base leading-relaxed text-foreground/90 md:text-lg">
                      {UI[lang].subhead}
                    </p>

                    <div className="mt-6 flex flex-wrap items-center gap-2">
                      <span
                        className="rounded-full border border-border bg-background/60 px-3 py-1 text-xs backdrop-blur"
                        style={{ fontFamily: "var(--font-mono)" }}
                      >
                        {UI[lang].host}: <span className="font-medium">{data.podcast.host}</span>
                      </span>
                      <span
                        className="rounded-full border border-border bg-background/60 px-3 py-1 text-xs backdrop-blur"
                        style={{ fontFamily: "var(--font-mono)" }}
                      >
                        {UI[lang].guest}: <span className="font-medium">{data.podcast.guest}</span>
                      </span>
                    </div>
                  </div>

                  {/* Small cover as secondary metadata element */}
                  <div className="hidden md:block">
                    <div className="overflow-hidden rounded-2xl border border-border bg-background/70 shadow-sm">
                      <img src={coverUrl} alt="Podcast cover" className="h-[170px] w-[170px] object-cover" />
                    </div>
                    <div
                      className="mt-2 text-[11px] text-muted-foreground"
                      style={{ fontFamily: "var(--font-mono)" }}
                    >
                      {data.podcast.show}
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Highlights */}
            <section className="space-y-10">
              {data.highlights.map((h, idx) => {
                const playing = nowPlaying === h.id;
                const paused = playing && isPaused;
                return (
                  <article
                    key={h.id}
                    id={h.id}
                    className="scroll-mt-10 rounded-[26px] border border-border bg-card/60 p-6 backdrop-blur md:p-8"
                  >
                    <header className="flex flex-col gap-6 md:flex-row md:items-start md:justify-between">
                      <div className="min-w-0">
                        <div className="flex items-baseline gap-4">
                          <div
                            className="text-[46px] leading-none text-primary md:text-[64px]"
                            style={{ fontFamily: displayFont(lang) }}
                          >
                            {String(idx + 1).padStart(2, "0")}
                          </div>
                          <div className="min-w-0">
                            <div
                              className="text-xs uppercase tracking-[0.22em] text-muted-foreground"
                              style={{ fontFamily: "var(--font-mono)" }}
                            >
                              {formatTimecode(h.start)}
                            </div>
                            <h2
                              className="mt-2 text-2xl leading-[1.05] md:text-3xl"
                              style={{ fontFamily: displayFont(lang) }}
                            >
                              {titleFor(h, lang)}
                            </h2>
                          </div>
                        </div>

                        <p className="mt-4 max-w-3xl text-sm leading-relaxed text-muted-foreground">
                          {t(h, lang, "context")}
                        </p>
                      </div>

                      <div className="flex shrink-0 items-center gap-2">
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              onClick={() => play(h.id)}
                              className="h-11 rounded-full px-4"
                            >
                              {playing && !paused ? (
                                <Pause className="mr-2 h-4 w-4" />
                              ) : (
                                <Play className="mr-2 h-4 w-4" />
                              )}
                              {playing && !paused ? UI[lang].pause : UI[lang].playClip}
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            {lang === "en"
                              ? "Plays the original audio from this moment."
                              : lang === "ja"
                                ? "この部分の原音クリップを再生します。"
                                : "播放这一段的原声音频。"}
                          </TooltipContent>
                        </Tooltip>

                        <Button
                          asChild
                          variant="outline"
                          className="h-11 rounded-full border-border bg-background/60 px-4 text-sm backdrop-blur"
                        >
                          <Link href={`/top`}>{UI[lang].backToTop}</Link>
                        </Button>
                      </div>
                    </header>

                    <Separator className="my-6" />

                    <div className="grid gap-6 md:grid-cols-[1.2fr_0.9fr]">
                      {/* Quote (translation primary; EN preserved as secondary) */}
                      <div className="relative">
                        <div
                          className="absolute -left-2 -top-4 select-none text-[120px] leading-none text-foreground/5 md:text-[160px]"
                          style={{ fontFamily: displayFont(lang) }}
                        >
                          “
                        </div>

                        <blockquote
                          className={cn(
                            "relative",
                            lang === "en" ? "text-lg leading-relaxed md:text-xl" : "text-[17px] leading-[1.9] md:text-[19px] md:leading-[2.0]",
                            "max-w-[58ch]"
                          )}
                          style={{ fontFamily: displayFont(lang) }}
                        >
                          {t(h, lang, "quote")}
                        </blockquote>

                        {lang !== "en" && (
                          <div className="mt-4 max-w-[62ch]">
                            <Collapsible
                              open={!!openOriginal[h.id]}
                              onOpenChange={(open) =>
                                setOpenOriginal((prev) => ({ ...prev, [h.id]: open }))
                              }
                            >
                              <CollapsibleTrigger asChild>
                                <button
                                  className="group inline-flex items-center gap-2 rounded-full border border-border bg-background/60 px-3 py-1 text-[11px] text-muted-foreground backdrop-blur transition-colors hover:bg-background"
                                  style={{ fontFamily: "var(--font-mono)" }}
                                  type="button"
                                >
                                  <span>{UI[lang].originalEn}</span>
                                  <span className="text-foreground/60">•</span>
                                  <span className="text-foreground/70">
                                    {openOriginal[h.id] ? UI[lang].hideOriginal : UI[lang].showOriginal}
                                  </span>
                                  <ChevronDown
                                    className={cn(
                                      "h-3.5 w-3.5 transition-transform",
                                      openOriginal[h.id] ? "rotate-180" : "rotate-0"
                                    )}
                                  />
                                </button>
                              </CollapsibleTrigger>
                              <CollapsibleContent>
                                <div className="mt-3 rounded-2xl border border-border bg-background/60 p-4">
                                  <div
                                    className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground"
                                    style={{ fontFamily: "var(--font-mono)" }}
                                  >
                                    {UI.en.originalEn}
                                  </div>
                                  <div
                                    className="mt-2 text-sm leading-relaxed text-foreground/80"
                                    style={{ fontFamily: displayFont("en") }}
                                  >
                                    {t(h, "en", "quote")}
                                  </div>
                                </div>
                              </CollapsibleContent>
                            </Collapsible>
                          </div>
                        )}

                        <div
                          className="mt-5 flex flex-wrap items-center gap-2 text-xs text-muted-foreground"
                          style={{ fontFamily: "var(--font-mono)" }}
                        >
                          <span className="rounded-full bg-secondary px-2 py-1">{UI[lang].timestamp}</span>
                          <span className="rounded-full bg-secondary px-2 py-1">{formatTimecode(h.start)} → {formatTimecode(h.end)}</span>
                        </div>
                      </div>

                      {/* Takeaway */}
                      <div className="md:pl-2">
                        <Card className="rounded-2xl border-border bg-background/70 p-5">
                          <div
                            className="text-xs uppercase tracking-[0.22em] text-muted-foreground"
                            style={{ fontFamily: "var(--font-mono)" }}
                          >
                            {UI[lang].takeaway}
                          </div>
                          <p className="mt-3 text-sm leading-relaxed text-foreground">{t(h, lang, "takeaway")}</p>
                        </Card>

                        <div
                          className="mt-4 text-[11px] text-muted-foreground"
                          style={{ fontFamily: "var(--font-mono)" }}
                        >
                          {data.podcast.show}
                        </div>
                      </div>
                    </div>
                  </article>
                );
              })}
            </section>

            {/* Closing */}
            <section className="rounded-[28px] border border-border bg-background/60 p-6 backdrop-blur md:p-8">
              <div
                className="text-xs uppercase tracking-[0.22em] text-muted-foreground"
                style={{ fontFamily: "var(--font-mono)" }}
              >
                {UI[lang].closingEyebrow}
              </div>
              <h2
                className="mt-3 text-3xl leading-[1.05] md:text-4xl"
                style={{ fontFamily: displayFont(lang) }}
              >
                {UI[lang].closingTitle}
              </h2>

              <ul className="mt-6 space-y-3 text-sm leading-relaxed">
                {(lang === "en"
                  ? data.closing.bullets_en
                  : lang === "ja"
                    ? data.closing.bullets_ja
                    : data.closing.bullets_zh
                ).map((b: string, i: number) => (
                  <li key={i} className="flex gap-3">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    <span>{b}</span>
                  </li>
                ))}
              </ul>

              <Separator className="my-7" />

              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="text-xs text-muted-foreground" style={{ fontFamily: "var(--font-mono)" }}>
                  {UI[lang].curated}
                </div>
                <a
                  className="inline-flex items-center gap-2 rounded-full border border-border bg-card/70 px-4 py-2 text-xs"
                  href={data.podcast.source_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  <span style={{ fontFamily: "var(--font-mono)" }}>{UI[lang].listenFull}</span>
                  <ArrowUpRight className="h-4 w-4" />
                </a>
              </div>
            </section>

            <footer className="pb-10 text-xs text-muted-foreground" style={{ fontFamily: "var(--font-mono)" }}>
              {lang === "en"
                ? "Built as an editorial reading experience. Quotes are selected from an automated transcript and may include minor transcription artifacts."
                : lang === "ja"
                  ? "編集記事として読める体験を目指して構成しました。引用は自動文字起こしをもとにしており、軽微な転写の揺れが含まれる可能性があります。"
                  : "这是一个偏编辑式的阅读页面。引用来自自动转写文本，可能包含少量转写误差。"}
            </footer>
          </main>
        </div>
      </div>
    </div>
  );
}
