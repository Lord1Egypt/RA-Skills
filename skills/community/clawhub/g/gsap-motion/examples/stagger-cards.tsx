"use client";

import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

type RankedItem = {
  id: string;
  rank: number;
  title: string;
  imageUrl: string;
};

type RankingGridProps = {
  items: RankedItem[];
};

export function RankingGrid({ items }: RankingGridProps) {
  const root = useRef<HTMLDivElement | null>(null);

  useGSAP(
    () => {
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      if (reduceMotion) {
        gsap.set("[data-ranking-card]", { opacity: 1, y: 0, scale: 1 });
        return;
      }

      gsap.from("[data-ranking-card]", {
        opacity: 0,
        y: 18,
        scale: 0.98,
        duration: 0.36,
        ease: "power2.out",
        stagger: { each: 0.045, from: "start" },
      });
    },
    { scope: root, dependencies: [items.length], revertOnUpdate: true },
  );

  return (
    <div ref={root} className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
      {items.map((item) => (
        <article
          key={item.id}
          data-ranking-card
          className="group relative aspect-[3/4] overflow-hidden rounded-lg bg-neutral-900 text-white"
        >
          <img src={item.imageUrl} alt="" className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/20 to-transparent" />
          <div className="absolute inset-x-0 bottom-0 p-3">
            <p className="text-4xl font-black leading-none text-lime-300">#{item.rank}</p>
            <h3 className="mt-1 line-clamp-2 text-sm font-bold leading-tight">{item.title}</h3>
          </div>
        </article>
      ))}
    </div>
  );
}
