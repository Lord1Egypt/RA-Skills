"use client";

import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger, useGSAP);

const chapters = [
  { id: "taste", label: "Taste", text: "Choose the things that define your profile." },
  { id: "rank", label: "Rank", text: "Build from Top 5 toward Top 100 at your own pace." },
  { id: "share", label: "Share", text: "Compare preferences and discover overlaps." },
];

export function ScrollStorytelling() {
  const root = useRef<HTMLElement | null>(null);

  useGSAP(
    () => {
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      if (reduceMotion) {
        gsap.set("[data-story-card]", { opacity: 1, y: 0 });
        return;
      }

      const mm = gsap.matchMedia();

      mm.add("(min-width: 768px)", () => {
        const cards = gsap.utils.toArray<HTMLElement>("[data-story-card]");

        cards.forEach((card, index) => {
          gsap.fromTo(
            card,
            { opacity: index === 0 ? 1 : 0.35, y: 20 },
            {
              opacity: 1,
              y: 0,
              ease: "none",
              scrollTrigger: {
                trigger: card,
                start: "top 70%",
                end: "bottom 35%",
                scrub: true,
              },
            },
          );
        });

        gsap.to("[data-story-progress]", {
          scaleY: 1,
          transformOrigin: "top",
          ease: "none",
          scrollTrigger: {
            trigger: root.current,
            start: "top center",
            end: "bottom center",
            scrub: true,
          },
        });
      });

      mm.add("(max-width: 767px)", () => {
        gsap.from("[data-story-card]", {
          opacity: 0,
          y: 18,
          duration: 0.4,
          ease: "power2.out",
          stagger: 0.05,
          scrollTrigger: {
            trigger: root.current,
            start: "top 75%",
            once: true,
          },
        });
      });

      return () => mm.revert();
    },
    { scope: root },
  );

  return (
    <section ref={root} className="relative bg-neutral-950 px-5 py-20 text-white md:px-8">
      <div className="mx-auto grid max-w-5xl gap-8 md:grid-cols-[8px_1fr]">
        <div className="hidden overflow-hidden rounded-full bg-white/15 md:block">
          <div data-story-progress className="h-full w-full origin-top scale-y-0 rounded-full bg-lime-300" />
        </div>
        <div className="grid gap-5">
          {chapters.map((chapter, index) => (
            <article key={chapter.id} data-story-card className="rounded-lg border border-white/12 bg-white/8 p-5">
              <p className="text-5xl font-black leading-none text-lime-300">0{index + 1}</p>
              <h2 className="mt-4 text-2xl font-black">{chapter.label}</h2>
              <p className="mt-2 max-w-xl text-white/76">{chapter.text}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
