"use client";

import { useMemo, useRef, useState } from "react";
import gsap from "gsap";
import { Flip } from "gsap/Flip";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(Flip, useGSAP);

type Item = {
  id: string;
  rank: number;
  title: string;
  category: "movies" | "music" | "books";
};

const initialItems: Item[] = [
  { id: "interstellar", rank: 1, title: "Interstellar", category: "movies" },
  { id: "blonde", rank: 2, title: "Blonde", category: "music" },
  { id: "dune", rank: 3, title: "Dune", category: "books" },
  { id: "arrival", rank: 4, title: "Arrival", category: "movies" },
];

export function FlipRankingFilter() {
  const root = useRef<HTMLDivElement | null>(null);
  const [filter, setFilter] = useState<"all" | Item["category"]>("all");
  const { contextSafe } = useGSAP({ scope: root });

  const visibleItems = useMemo(() => {
    return filter === "all" ? initialItems : initialItems.filter((item) => item.category === filter);
  }, [filter]);

  const updateFilter = contextSafe((nextFilter: "all" | Item["category"]) => {
    if (!root.current) return;

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const state = Flip.getState("[data-flip-card]", { props: "opacity" });

    setFilter(nextFilter);

    requestAnimationFrame(() => {
      if (reduceMotion) return;

      Flip.from(state, {
        targets: "[data-flip-card]",
        duration: 0.42,
        ease: "power2.out",
        absolute: true,
        onEnter: (elements) => gsap.fromTo(elements, { opacity: 0, scale: 0.96 }, { opacity: 1, scale: 1, duration: 0.25 }),
        onLeave: (elements) => gsap.to(elements, { opacity: 0, scale: 0.96, duration: 0.2 }),
      });
    });
  });

  return (
    <div ref={root} className="space-y-5">
      <div className="flex flex-wrap gap-2">
        {(["all", "movies", "music", "books"] as const).map((option) => (
          <button
            key={option}
            type="button"
            onClick={() => updateFilter(option)}
            className="rounded-full border border-neutral-300 px-4 py-2 text-sm font-bold capitalize text-neutral-900 data-[active=true]:border-neutral-950 data-[active=true]:bg-neutral-950 data-[active=true]:text-white"
            data-active={filter === option}
          >
            {option}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {visibleItems.map((item) => (
          <article key={item.id} data-flip-card className="rounded-lg bg-neutral-950 p-4 text-white">
            <p className="text-4xl font-black text-lime-300">#{item.rank}</p>
            <h3 className="mt-4 text-lg font-black leading-tight">{item.title}</h3>
            <p className="mt-1 text-sm capitalize text-white/62">{item.category}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
