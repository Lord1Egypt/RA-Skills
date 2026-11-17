"use client";

import { useEffect, useState } from "react";
import gsap from "gsap";

export function usePrefersReducedMotion() {
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(query.matches);

    const onChange = () => setReduced(query.matches);
    query.addEventListener("change", onChange);

    return () => query.removeEventListener("change", onChange);
  }, []);

  return reduced;
}

export function playSelectionFeedback(target: HTMLElement, reducedMotion: boolean) {
  gsap.killTweensOf(target);

  if (reducedMotion) {
    gsap.fromTo(target, { opacity: 0.72 }, { opacity: 1, duration: 0.16, ease: "none" });
    return;
  }

  gsap.fromTo(
    target,
    { scale: 0.96 },
    {
      scale: 1,
      duration: 0.28,
      ease: "back.out(1.8)",
      overwrite: "auto",
    },
  );
}

type ChoiceButtonProps = {
  label: string;
  selected: boolean;
  onSelect: () => void;
};

export function ChoiceButton({ label, selected, onSelect }: ChoiceButtonProps) {
  const reducedMotion = usePrefersReducedMotion();

  return (
    <button
      type="button"
      aria-pressed={selected}
      onClick={(event) => {
        playSelectionFeedback(event.currentTarget, reducedMotion);
        onSelect();
      }}
      className="rounded-full border border-neutral-300 px-4 py-2 text-sm font-bold text-neutral-950 transition-colors aria-pressed:border-lime-500 aria-pressed:bg-lime-200"
    >
      {label}
    </button>
  );
}
