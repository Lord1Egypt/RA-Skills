import React from "react";
import "./Card.css";

type CardProps = {
  title?: string;
  subtitle?: string;
  footer?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
};

export function Card({ title, subtitle, footer, children, className = "" }: CardProps) {
  return (
    <section className={["card", className].filter(Boolean).join(" ")}>
      {(title || subtitle) && (
        <header className="card__header">
          {title ? <div className="card__title">{title}</div> : null}
          {subtitle ? <div className="card__subtitle">{subtitle}</div> : null}
        </header>
      )}
      <div className="card__body">{children}</div>
      {footer ? <footer className="card__footer">{footer}</footer> : null}
    </section>
  );
}
