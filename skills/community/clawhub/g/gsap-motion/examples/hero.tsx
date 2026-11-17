"use client";

import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

type HeroProps = {
  title: string;
  subtitle: string;
  imageUrl: string;
};

export function MotionHero({ title, subtitle, imageUrl }: HeroProps) {
  const root = useRef<HTMLElement | null>(null);

  useGSAP(
    () => {
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      if (reduceMotion) {
        gsap.set("[data-hero-animate]", { opacity: 1, y: 0, scale: 1 });
        return;
      }

      const tl = gsap.timeline({
        defaults: { duration: 0.48, ease: "power2.out" },
      });

      tl.from("[data-hero-media]", { opacity: 0, scale: 0.96, duration: 0.65 })
        .from("[data-hero-rank]", { opacity: 0, y: 12, scale: 0.9 }, "-=0.35")
        .from("[data-hero-title]", { opacity: 0, y: 18 }, "-=0.25")
        .from("[data-hero-copy]", { opacity: 0, y: 12 }, "-=0.2")
        .from("[data-hero-action]", { opacity: 0, y: 10 }, "-=0.12");
    },
    { scope: root },
  );

  return (
    <section ref={root} className="relative min-h-[82svh] overflow-hidden bg-neutral-950 text-white">
      <img
        data-hero-media
        data-hero-animate
        src={imageUrl}
        alt=""
        className="absolute inset-0 h-full w-full object-cover opacity-80"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/35 to-transparent" />

      <div className="relative flex min-h-[82svh] max-w-5xl flex-col justify-end px-5 pb-24 pt-24 md:px-8">
        <p data-hero-rank data-hero-animate className="text-7xl font-black leading-none text-lime-300 md:text-9xl">
          #1
        </p>
        <h1 data-hero-title data-hero-animate className="mt-3 max-w-3xl text-5xl font-black leading-none md:text-7xl">
          {title}
        </h1>
        <p data-hero-copy data-hero-animate className="mt-4 max-w-xl text-base leading-7 text-white/82 md:text-lg">
          {subtitle}
        </p>
        <button
          data-hero-action
          data-hero-animate
          className="mt-7 w-fit rounded-full bg-white px-5 py-3 text-sm font-bold text-neutral-950 transition-transform hover:scale-[1.03] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-white"
        >
          Start ranking
        </button>
      </div>
    </section>
  );
}
