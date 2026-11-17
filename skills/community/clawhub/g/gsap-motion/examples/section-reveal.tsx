"use client";

import { PropsWithChildren, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger, useGSAP);

type RevealSectionProps = PropsWithChildren<{
  eyebrow?: string;
  title: string;
}>;

export function RevealSection({ eyebrow, title, children }: RevealSectionProps) {
  const root = useRef<HTMLElement | null>(null);

  useGSAP(
    () => {
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      if (reduceMotion) {
        gsap.set("[data-reveal]", { opacity: 1, y: 0 });
        return;
      }

      gsap.from("[data-reveal]", {
        opacity: 0,
        y: 24,
        duration: 0.5,
        ease: "power2.out",
        stagger: 0.06,
        scrollTrigger: {
          trigger: root.current,
          start: "top 74%",
          once: true,
        },
      });
    },
    { scope: root },
  );

  return (
    <section ref={root} className="px-5 py-16 md:px-8 md:py-24">
      <div className="mx-auto max-w-5xl">
        {eyebrow ? (
          <p data-reveal className="text-sm font-bold uppercase tracking-wide text-rose-600">
            {eyebrow}
          </p>
        ) : null}
        <h2 data-reveal className="mt-2 max-w-2xl text-3xl font-black leading-tight text-neutral-950 md:text-5xl">
          {title}
        </h2>
        <div data-reveal className="mt-8">
          {children}
        </div>
      </div>
    </section>
  );
}
