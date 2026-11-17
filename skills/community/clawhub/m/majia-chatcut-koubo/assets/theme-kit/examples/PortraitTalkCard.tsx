import type { ReactNode } from "react";
import "../tokens/themes.css";
import "../components/portrait-talk-card.css";
import type { PortraitLayoutId, PortraitThemeId } from "../tokens/themes";

type Props = {
  theme?: PortraitThemeId;
  layout?: PortraitLayoutId;
  eyebrow?: string;
  title: ReactNode;
  lead?: string;
  emphasis: string;
  cta?: string;
  footer?: string;
  speaker?: ReactNode;
};

export function PortraitTalkCard({
  theme = "deep-space-blue",
  layout = "diagonal-tech",
  eyebrow = "连锁餐饮 AI 实战",
  title,
  lead = "真正决定结果的是",
  emphasis,
  cta = "查看结论",
  footer = "先补数据，再谈模型",
  speaker,
}: Props) {
  return (
    <article className="talk-card" data-theme={theme} data-layout={layout}>
      <div className="talk-card__background" aria-hidden="true" />
      <div className="talk-card__ambient" aria-hidden="true" />
      <div className="talk-card__eyebrow">{eyebrow}</div>
      <h1 className="talk-card__title">{title}</h1>
      <p className="talk-card__lead">{lead}</p>
      <p className="talk-card__emphasis">{emphasis}</p>
      <div className="talk-card__cta">{cta}</div>
      <div className="talk-card__speaker is-cutout">{speaker ?? <div className="talk-card__speaker-figure" />}</div>
      <div className="talk-card__footer">{footer}</div>
    </article>
  );
}
